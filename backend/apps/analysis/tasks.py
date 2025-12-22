from celery import shared_task
from django.conf import settings
from apps.resumes.models import Resume
from apps.jobs.models import JobPosting
from apps.analysis.models import AnalysisResult
from .utils.parsers import PDFParser
from .utils.crawlers import JobCrawler
from .utils.llm_client import LLMClient
import logging

logger = logging.getLogger(__name__)


@shared_task
def analyze_application_task(resume_id, job_posting_id, user_id):
    try:
        resume = Resume.objects.get(id=resume_id)
        job_posting = JobPosting.objects.get(id=job_posting_id)

        if not resume.parsed_content:
            parser = PDFParser()
            resume.parsed_content = parser.parse(resume.file_path)
            resume.save()

        if not job_posting.content:
            crawler = JobCrawler()
            job_posting.content = crawler.fetch(job_posting.url)
            job_posting.save()

        # settings.py에서 설정한 GRADIO_URL 사용
        llm = LLMClient(settings.GRADIO_URL)

        analysis_data = llm.analyze_gap(resume.parsed_content, job_posting.content)

        # [FIX] LLM 응답 구조가 플랫/중첩 둘 다 올 수 있으므로 호환성 확보
        
        # 1. 중첩 구조 가져오기 (없으면 빈 딕셔너리)
        user_analysis = analysis_data.get('user_analysis', {})
        jd_analysis = analysis_data.get('jd_analysis', {})
        gap_analysis = analysis_data.get('gap_analysis', {})

        # 2. 데이터 추출 (Flat 우선 확인 -> 없으면 중첩 확인)
        extracted_skills = analysis_data.get('extracted_skills') or user_analysis.get('extracted_skills', [])
        
        company_name = analysis_data.get('company_name') or jd_analysis.get('company_name', job_posting.company)
        company_description = analysis_data.get('company_description') or jd_analysis.get('company_description', '')
        jd_skills = analysis_data.get('jd_skills') or jd_analysis.get('required_skills', [])
        main_tasks = analysis_data.get('main_tasks') or jd_analysis.get('main_tasks', [])
        
        # Gap Analysis는 보통 중첩되어 오지만, 혹시 모르니 Flat도 체크
        score = gap_analysis.get('score') if gap_analysis.get('score') is not None else analysis_data.get('score', 0)
        reasoning = gap_analysis.get('reasoning') or analysis_data.get('reasoning', '')
        missing_skills = gap_analysis.get('missing_skills') or analysis_data.get('missing_skills', [])
        missing_chapters = gap_analysis.get('missing_skills_chapters') or analysis_data.get('missing_skills_chapters', [])

        # 3. JobPosting 정보 업데이트 (분석된 회사명/내용 반영)
        if company_name and job_posting.company in ['분석중...', '']:
            job_posting.company = company_name
            job_posting.title = f"{company_name} 채용공고" # 제목도 임시로 업데이트
            job_posting.save()

        # 4. 결과 저장
        AnalysisResult.objects.create(
            user_id=user_id,
            resume=resume,
            job_posting=job_posting,
            user_extracted_skills=extracted_skills,
            company_name=company_name,
            jd_required_skills=jd_skills,
            jd_main_tasks=main_tasks,
            score=score,
            reasoning=reasoning,
            gap_missing_skills=missing_skills,
            gap_missing_chapters=missing_chapters
        )

        logger.info(f"Analysis completed for User {user_id}")
        logger.info(f"Raw Analysis Data: {analysis_data}")

    except Exception as e:
        logger.error(f"Analysis task failed: {e}")