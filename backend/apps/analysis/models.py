from django.db import models
from django.conf import settings


class AnalysisResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    resume = models.ForeignKey('resumes.Resume', on_delete = models.SET_NULL, null = True)
    job_posting = models.ForeignKey('jobs.JobPosting', on_delete = models.CASCADE)

    # [JSON: user_analysis]
    user_extracted_skills = models.JSONField(default = list, verbose_name = "보유 기술 목록")

    # [JSON: jd_analysis]
    company_name = models.CharField(max_length = 100, blank = True, verbose_name = "분석된 회사명")
    jd_required_skills = models.JSONField(default = list, verbose_name = "JD 요구 기술 목록")
    jd_main_tasks = models.JSONField(default = list, verbose_name = "주요 업무 목록")

    # [JSON: gap_analysis]
    score = models.IntegerField(default = 0, verbose_name = "적합도 점수")
    reasoning = models.TextField(blank = True, verbose_name = "분석 결과 및 근거")
    gap_missing_skills = models.JSONField(default = list, verbose_name = "부족한 기술 목록")
    gap_missing_chapters = models.JSONField(default = list, verbose_name = "추천 학습 챕터 목록")

    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'analysis_results'