import re

import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

import datetime
import os

__all__ = (
    'PickyUser',
)


class PickyUserManager(BaseUserManager):
    # 확인 완료 8/10 joe
    def create_user(self, email, nickname, password, img_profile=None, content=None):
        user = self.model(
                email=self.normalize_email(email),
                nickname=nickname,
                content=content,
                img_profile=img_profile,
        )
        # set_password AbstractBaseUser 내장함수
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

    # facebook 유저 생성 8/16 joe
    def create_facebook_user(self, user_info):
        user, user_created = self.get_or_create(
                fb_id=user_info['id'],
                nickname=user_info.get('name', ''),
                email=user_info.get('email', ''),
                id_type=PickyUser.USER_TYPE_FACEBOOK,
        )
        if user_created and user_info.get('picture'):
            url_picture = user_info['picture']['data']['url']
            p = re.compile(r'.*\.([^?]+)')
            file_ext = re.search(p, url_picture).group(1)
            file_name = '{}.{}'.format(
                    user.pk,
                    file_ext,
            )
            # 이미지파일을 임시저장할 객체. delete=True(기본값) 로컬변수가 사라지는 순간 삭제됨
            temp_file = NamedTemporaryFile(delete=True)
            # 프로필 이미지 url에 대한 get 요청(이미지 다운로드)
            response = requests.get(url_picture)
            # 요청 결과를 temp_file에 기록
            temp_file.write(response.content)
            # ImageField의 save()메서드를 호출해서 해당 임시파일객체를 주어진 이름의 파일로 저장
            # 저장하는 파일명은 위에서 만든 <유저pk.주어진파일확장자> 를 사용
            user.img_profile.save(file_name, File(temp_file))
        return user


# user image 저장폴더이름 지정 - user email의 특수문자를 제외한 폴더에 이미지 저장
# 저장되는 파일이름은 nickname-날짜-밀리세컨드.기존확장자
def user_img_directory(instance, filename):
    # 이메일이 없거나 빈값이면 pk + 닉네임으로 폴더 생성 (페이스북에 이메일없는 계정이 있음)
    if not instance.email or instance.email == '':
        folder_name = instance.pk + instance.nickname.replace(" ", "_")
    # 이메일이 있으면
    else:
        folder_name = instance.email.replace("@", "_").replace(".", "_")

    filename = '{nickname}-{date}-{microsecond}{extension}'.format(
            nickname=instance.nickname,
            date=datetime.datetime.now().strftime('%Y-%m-%d'),
            microsecond=datetime.datetime.now().microsecond,
            extension=os.path.splitext(filename)[1],
    )
    return 'user/{dir}/{filename}'.format(dir=folder_name, filename=filename)


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

    email = models.EmailField(
            verbose_name='email',
            max_length=250,
            unique=True,
    )
    nickname = models.CharField(
            max_length=100,
            unique=True
    )
    password = models.CharField(
            max_length=200,
    )
    img_profile = models.ImageField(
            # 위의 user_img_directory 함수에서 정해진 폴더에 저장
            upload_to=user_img_directory,
            blank=True,
            null=True,
            max_length=250,
    )
    # user 인삿말
    content = models.TextField(blank=True, null=True)
    id_type = models.CharField(
            max_length=1,
            choices=USER_TYPE_CHOICES,
            default=USER_TYPE_PICKY,
            )
    # facebook user_id 8/16 joe
    fb_id = models.CharField(max_length=100, blank=True, null=True)
    # 활성화된 유저인가? admin 페이지때문에 필수 : 8/1 Joe
    is_active = models.BooleanField(default=True)
    # 관리자인가? admin 페이지때문에 필수 : 8/1 Joe
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

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
