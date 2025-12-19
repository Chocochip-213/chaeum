from django.db import models
from django.conf import settings

class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    file_path = models.CharField(max_length=512, verbose_name="PDF 파일 경로")
    parsed_content = models.TextField(blank=True, verbose_name="텍스트 추출 원본")
    status = models.CharField(max_length=20, default='PENDING', verbose_name="분석 상태") # PENDING, SUCCESS
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resumes'