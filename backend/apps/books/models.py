from django.db import models
from pgvector.django import VectorField
from django.conf import settings


class Book(models.Model):
    id = models.BigAutoField(primary_key = True)
    title = models.CharField(max_length = 512)
    author = models.CharField(max_length = 256)
    isbn = models.CharField(max_length = 13, unique = True)
    summary = models.TextField(blank = True, null = True)

    subtitle = models.CharField(max_length = 512, blank = True, null = True)
    publisher = models.CharField(max_length = 256)
    publication_date = models.DateField(null = True, blank = True)
    page_count = models.IntegerField(default = 0, null = True, blank = True)

    full_description = models.TextField(blank = True, null = True)
    publisher_description = models.TextField(blank = True, null = True)
    authors_json = models.JSONField(blank = True, null = True)

    created_at = models.DateTimeField(auto_now_add = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, null = True)
    raw_toc = models.TextField(blank = True, null = True)

    class Meta:
        db_table = 'books'
        managed = True


class TOCChunk(models.Model):
    book = models.ForeignKey(Book, on_delete = models.CASCADE, related_name = 'chunks', db_column = 'isbn', to_field = 'isbn')

    level = models.IntegerField(default = 0, help_text = "목차 레벨")
    number = models.CharField(max_length = 50, blank = True, null = True, help_text = "목차 순서/번호")

    chapter_title = models.CharField(max_length = 255)
    composite_text = models.TextField(help_text = "RAG 검색용 텍스트")
    embedding = VectorField(dimensions = 768)

    class Meta:
        db_table = 'toc_chunks'


class Store(models.Model):
    name = models.CharField(max_length = 100)  # 예: 가로수길점
    branch_code = models.CharField(max_length = 20, unique = True)  # 내부 관리 코드 (SEOUL_01)
    off_code = models.CharField(max_length = 50, null = True, blank = True)  # 알라딘 API 매핑 코드 (Gangnam)
    address = models.CharField(max_length = 255)
    lat = models.FloatField(null = True)  # 위도
    lon = models.FloatField(null = True)  # 경도

    class Meta:
        db_table = 'stores'

    def __str__(self):
        return self.name