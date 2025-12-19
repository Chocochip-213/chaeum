from django.db import models
from django.conf import settings

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    # Book앱의 Book 모델 참조를 위한 IntegerField 또는 느슨한 연결 권장 (여기서는 문자열 관계 유지 가능)
    # 하지만 ERD상 FK이므로 Book 모델 참조
    # 순환 참조 방지를 위해 문자열로 앱.모델 명시
    book = models.ForeignKey('books.Book', on_delete=models.SET_NULL, null=True, blank=True, db_column='book_isbn')
    title = models.CharField(max_length=255)
    content = models.TextField()
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'