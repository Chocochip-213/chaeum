from django.db import models
from django.conf import settings

class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    file_name = models.CharField(max_length=255, verbose_name="파일명")
    parsed_content = models.TextField(blank=True, verbose_name="텍스트 추출 원본")
    status = models.CharField(max_length=20, default='SUCCESS', verbose_name="분석 상태")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resumes'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.file_name}"