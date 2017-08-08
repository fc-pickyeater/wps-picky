import re

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import datetime
import os


__all__ = (
    'PickyUser',
)


class PickyUserManager(BaseUserManager):
    # create Manager : 작업하면서 내용 확인 필요 - 8/1 Joe
    def create_user(self, email, nickname, password, img_profile=None, content=None):
        if not email:
            raise ValueError('email을 입력하세요.')
        if not nickname:
            raise ValueError('Nickname을 입력하세요.')

        user = self.model(
                email=self.normalize_email(email),
                nickname=nickname,
                content=content,
                img_profile=img_profile,
        )
        user.set_password(password)
        user.save()
        return user

    # createsuperuser manager : 디버그모드에서 확인완료 - 8/1 Joe
    def create_superuser(self, email, nickname, password):
        user = self.create_user(
                email=email,
                password=password,
                nickname=nickname,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# user image 저장폴더이름 지정 - user email의 특수문자를 제외한 폴더에 이미지 저장
# 저장되는 파일이름은 nickname-날짜-밀리세컨드.기존확장자
def user_img_directory(instance, filename):
    plain_email = instance.email.replace("@", "_").replace(".", "_")
    filename = '{nickname}-{date}-{microsecond}{extension}'.format(
            nickname=instance.nickname,
            date=datetime.datetime.now().strftime('%Y-%m-%d'),
            microsecond=datetime.datetime.now().microsecond,
            extension=os.path.splitext(filename)[1],
    )
    return 'user/{dir}/{filename}'.format(dir=plain_email, filename=filename)


class PickyUser(AbstractBaseUser):
    USER_TYPE_PICKY = 'd'
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_KAKAO = 'k'
    USER_TYPE_NAVER = 'n'
    USER_TYPE_CHOICES = (
        (USER_TYPE_PICKY, 'Picky'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
        (USER_TYPE_KAKAO, 'Kakao'),
        (USER_TYPE_NAVER, 'Naver'),
    )

    # user id
    email = models.EmailField(
            verbose_name='email',
            max_length=100,
            unique=True
    )
    # user nickname
    nickname = models.CharField(
            max_length=100,
            unique=True
    )
    # password
    password = models.CharField(
            max_length=16,
    )
    # user 사진
    img_profile = models.ImageField(
            # upload_to='user/%Y/%m/',
            # 위의 user_img_directory 함수에서 정해진 폴더에 저장
            upload_to=user_img_directory,
            blank=True,
            null=True
    )
    # user 인삿말
    content = models.TextField(blank=True)
    # django user : d
    # facebook user : f
    # naver user : n
    # kakao user : k
    id_type = models.CharField(
            max_length=1,
            choices=USER_TYPE_CHOICES,
            default=USER_TYPE_PICKY,
            )
    # 활성화된 유저인가? admin 페이지때문에 필수 : 8/1 Joe
    is_active = models.BooleanField(default=True)
    # 관리자인가? admin 페이지때문에 필수 : 8/1 Joe
    is_admin = models.BooleanField(default=False)

    objects = PickyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'nickname',
    ]

    # admin 페이지때문에 필수 : 8/1 Joe
    def get_full_name(self):
        # The user is identified by their email address
        return self.nickname

    # admin 페이지때문에 필수 : 8/1 Joe
    def get_short_name(self):
        # The user is identified by their email address
        return self.nickname

    def __str__(self):
        return self.nickname

    # admin 페이지때문에 필수 : 8/1 Joe
    def has_perm(self, perm, obj=None):
        return True

    # admin 페이지때문에 필수 : 8/1 Joe
    def has_module_perms(self, app_label):
        return True

    # admin 페이지때문에 필수 : 8/1 Joe
    @property
    def is_staff(self):
        return self.is_admin


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

