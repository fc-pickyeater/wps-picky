from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

__all__ = (
    'PickyUser',
)


class PickyUserManager(BaseUserManager):
    # create Manager : 작업하면서 내용 확인 필요 - 8/1 Joe
    def create_user(self, email, nickname, password=None, img_profile=None, content=None):
        if not email:
            raise ValueError('email을 입력하세요.')

        user = self.model(
                email=self.normalize_email(email),
                nickname=nickname,
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


class PickyUser(AbstractBaseUser):
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
    # user 사진
    img_profile = models.ImageField(
            upload_to='media/user',
            blank=True,
            null=True
    )
    # user 인삿말
    content = models.TextField(blank=True)
    # django user : d
    # facebook user : f
    # naver user : n
    # kakao user : k
    id_type = models.CharField(default='d', max_length=1)
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
        return self.email

    # admin 페이지때문에 필수 : 8/1 Joe
    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

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
