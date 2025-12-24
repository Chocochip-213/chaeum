from rest_framework import views, status, parsers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.jobs.models import JobPosting
from apps.resumes.models import Resume
from .models import AnalysisResult
from .serializers import AnalysisResultSerializer
from .tasks import analyze_application_task
from .utils.parsers import PDFParser
from asgiref.sync import async_to_sync
from .services.rag_service import RAGService


class AnalysisView(views.APIView):
    permission_classes = [IsAuthenticated]

    # [중요] 파일 업로드를 처리하기 위한 파서 설정
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request):
        """
        분석 요청 (이력서 파일 + 채용공고 URL)
        """
        user = request.user
        job_posting_url = request.data.get('job_posting_url')
        resume_file = request.FILES.get('resume_file')

        # 1. 이력서 처리 (내용 비교 로직 추가)
        resume_id = None
        if resume_file:
            try:
                # 메모리 파싱
                file_bytes = resume_file.read()
                parser = PDFParser()
                parsed_content = parser.parse_stream(file_bytes)

                # 기존 이력서와 내용 비교
                latest_resume = Resume.objects.filter(user=user).last()

                if latest_resume and latest_resume.parsed_content == parsed_content:
                    # 내용이 완전히 같으면 기존 이력서 재사용 (ID 유지)
                    resume_id = latest_resume.id
                else:
                    # 내용이 다르면 기존 삭제 후 새로 생성
                    if latest_resume:
                        latest_resume.delete()

                    resume = Resume.objects.create(
                        user=user,
                        file_path="",
                        parsed_content=parsed_content,
                        status='SUCCESS'
                    )
                    resume_id = resume.id

            except Exception as e:
                return Response({"error": f"PDF parsing failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 파일 없으면 기존 이력서 사용
            latest_resume = Resume.objects.filter(user=user).last()
            if not latest_resume:
                return Response({"error": "No resume provided and no existing resume found."},
                                status=status.HTTP_400_BAD_REQUEST)
            resume_id = latest_resume.id

        # 2. 채용공고 처리 (URL로 JobPosting 찾기)
        job_posting_id = request.data.get('job_posting_id')

        # [수정] URL로 기존 JobPosting 찾기 (중복 분석 방지 핵심)
        if not job_posting_id and job_posting_url:
            # get_or_create를 사용하여 URL에 해당하는 공고가 있으면 가져오고, 없으면 만듬.
            job_posting, created = JobPosting.objects.get_or_create(
                url=job_posting_url,
                defaults={'title': '분석중...', 'company': '분석중...', 'content': ''}
            )
            job_posting_id = job_posting.id

        if not job_posting_id:
            return Response({"error": "job_posting_url is required"}, status=status.HTTP_400_BAD_REQUEST)

        # - 이력서 내용이 같으면 resume_id가 같으므로 캐싱된 결과가 반환됨!
        existing_result = AnalysisResult.objects.filter(
            user=user,
            resume_id=resume_id,
            job_posting_id=job_posting_id
        ).last()

        if existing_result:
            # 이미 결과가 있으면 즉시 반환 (200 OK)
            return Response({
                "message": "Analysis already exists",
                "result_id": existing_result.id,
                "cached": True
            }, status=status.HTTP_200_OK)

        # 4. Task 실행 (결과가 없을 때만)
        task = analyze_application_task.delay(
            resume_id=resume_id,
            job_posting_id=job_posting_id,
            user_id=user.id
        )

        return Response({"message": "Analysis started", "task_id": task.id}, status=status.HTTP_202_ACCEPTED)



    def get(self, request):
        """
        분석 결과 조회 + RAG 추천 도서 포함
        """
        user = request.user
        job_posting_url = request.query_params.get('job_posting_url')
        job_posting_id = request.query_params.get('job_posting_id')

        # 1. 이력서 ID 자동 추론
        latest_resume = Resume.objects.filter(user=user).last()
        if not latest_resume:
            return Response({"error": "No resume found"}, status=status.HTTP_404_NOT_FOUND)
        resume_id = latest_resume.id

        # 2. 공고 URL -> ID 변환
        if job_posting_url and not job_posting_id:
            try:
                job_posting = JobPosting.objects.get(url=job_posting_url)
                job_posting_id = job_posting.id
            except JobPosting.DoesNotExist:
                return Response({"error": "Job posting not found"}, status=status.HTTP_404_NOT_FOUND)

        if job_posting_id:
            result = AnalysisResult.objects.filter(
                user=user,
                resume_id=resume_id,
                job_posting_id=job_posting_id
            ).last()

            if result:
                serializer = AnalysisResultSerializer(result)
                data = serializer.data

                try:
                    recommendations = async_to_sync(RAGService.recommend_chapters)(result.id)
                    data['rag_recommendations'] = recommendations
                except Exception as e:
                    print(f"RAG Error: {e}")
                    data['rag_recommendations'] = []
                    data['rag_error'] = str(e)

                return Response(data)
            else:
                return Response({"status": "pending", "message": "Analysis in progress"},
                                status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "job_posting_url is required"}, status=status.HTTP_400_BAD_REQUEST)

class AnalysisHistoryView(generics.ListAPIView):
    """
    내 분석 결과 히스토리 조회 (최신순)
    URL: GET /api/analysis/history/
    """
    serializer_class = AnalysisResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 내가 요청한 분석 결과만, 최신순 정렬
        return AnalysisResult.objects.filter(user=self.request.user).order_by('-created_at')