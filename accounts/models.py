# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30, unique=True)

    # related_name 추가
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # 기본적으로 user_set으로 불리는 것을 customuser_set으로 변경
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # 기본적으로 user_set으로 불리는 것을 customuser_set으로 변경
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )


class EmailVerification(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    def is_code_valid(self, code):
        # 코드의 유효성을 확인하는 로직 (예: 시간 제한)
        return self.code == code and (timezone.now() - self.created_at).seconds < 600