from django.contrib.auth.models import AbstractUser
from django.db import models

__all__ = (
    'PickyUser',
)


class PickyUser(AbstractUser):
    # 프로필 사진
    profile_image = models.ImageField()
    # 프로필 설명
    profile_content = models.TextField(max_length=256)
    # 타 사이트 아이디1
    another_id1 = models.CharField(max_length=50)
    # 타 사이트 아이디2
    another_id2 = models.CharField(max_length=50)
    # 닉네임
    nickname = models.CharField(max_length=30)
    # 아이디 타입 (로그인시 구분)
    id_type = models.CharField(max_length=30)
