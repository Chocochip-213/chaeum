from rest_framework import viewsets, permissions, parsers, status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Resume
from .serializers import ResumeSerializer
from apps.analysis.utils.parsers import PDFParser # 이력서 파싱 스크립트임.


class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        uploaded_file = self.request.FILES.get('file')
        if not uploaded_file:
            return

        parser = PDFParser()
        parsed_text = ""

        try:
            file_bytes = uploaded_file.read()
            parsed_text = parser.parse_stream(file_bytes)
        except Exception as e:
            print(f"Parsing Error: {e}")

        serializer.save(
            user=self.request.user,
            file_name=uploaded_file.name,
            parsed_content=parsed_text,
            status='SUCCESS'
        )

    @action(detail=False, methods=['post'], url_path='sample')
    def load_sample(self, request):
        """
        주어진 sample_id에 해당하는 이력서 데이터를 복사하여 현재 사용자의 이력서로 생성합니다.
        """
        sample_id = request.data.get('sample_id')
        if not sample_id:
            return Response({"error": "sample_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 원본 샘플 이력서 조회
        try:
            sample_resume = Resume.objects.get(id=sample_id)
        except Resume.DoesNotExist:
            return Response({"error": "Sample resume not found"}, status=status.HTTP_404_NOT_FOUND)

        # 새 이력서 생성 (복사)
        new_resume = Resume.objects.create(
            user=request.user,
            file_name=sample_resume.file_name,
            parsed_content=sample_resume.parsed_content,
            status='SUCCESS'
        )

        serializer = self.get_serializer(new_resume)
        return Response(serializer.data, status=status.HTTP_201_CREATED)