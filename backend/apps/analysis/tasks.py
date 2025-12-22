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

        user_analysis = analysis_data.get('user_analysis', {})
        jd_analysis = analysis_data.get('jd_analysis', {})
        gap_analysis = analysis_data.get('gap_analysis', {})

        AnalysisResult.objects.create(
            user_id=user_id,
            resume=resume,
            job_posting=job_posting,
            user_extracted_skills=user_analysis.get('extracted_skills', []),
            company_name=jd_analysis.get('company_name', job_posting.company),
            jd_required_skills=jd_analysis.get('required_skills', []),
            jd_main_tasks=jd_analysis.get('main_tasks', []),
            score=gap_analysis.get('score', 0),
            reasoning=gap_analysis.get('reasoning', ''),
            gap_missing_skills=gap_analysis.get('missing_skills', []),
            gap_missing_chapters=gap_analysis.get('missing_skills_chapters', [])
        )

        logger.info(f"Analysis completed for User {user_id}")
        logger.info(f"Raw Analysis Data: {analysis_data}")

    except Exception as e:
        logger.error(f"Analysis task failed: {e}")