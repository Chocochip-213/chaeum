from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="이메일 (ID)")
    nickname = models.CharField(max_length=50, verbose_name="닉네임")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="가입일")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        db_table = 'users'
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'

    CAMPUS_CHOICES = [
        ('서울 캠퍼스', '서울 캠퍼스'),
        ('대전 캠퍼스', '대전 캠퍼스'),
        ('광주 캠퍼스', '광주 캠퍼스'),
        ('구미 캠퍼스', '구미 캠퍼스'),
        ('부울경 캠퍼스', '부울경 캠퍼스'),
    ]
    
    campus = models.CharField(
        max_length=10, 
        choices=CAMPUS_CHOICES, 
        verbose_name="캠퍼스"
    )