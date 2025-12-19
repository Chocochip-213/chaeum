from django.db import models

class JobPosting(models.Model):
    url = models.CharField(max_length=512, unique=True, verbose_name="채용공고 URL")
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=100)
    content = models.TextField(verbose_name="스크래핑된 본문")
    crawled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'job_postings'