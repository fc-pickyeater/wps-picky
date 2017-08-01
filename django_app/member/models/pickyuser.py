from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

__all__ = (
    'PickyUser',
)


class PickyUserManager(BaseUserManager):
    # create Manager
    def create_user(self, email, nickname, password=None, profile_image=None, profile_content=None):
        if not email:
            raise ValueError('email을 입력하세요.')

        user = self.model(
                email=self.normalize_email(email),
                nickname=nickname,
        )
        user.set_password(password)
        user.save()
        return user

    # createsuperuser manager : 디버그모드에서 확인완료 - Joe
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
    email = models.EmailField(
            verbose_name='email',
            max_length=100,
            unique=True
    )
    nickname = models.CharField(
            max_length=100,
            unique=True
    )
    # django user : d
    # facebook user : f
    # naver user : n
    # kakao user : k
    id_type = models.CharField(default='d', max_length=1)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)

    objects = PickyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'nickname',
        # 'id_type'
    ]

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

# class PickyUser(AbstractUser):
#     # 프로필 사진
#     profile_image = models.ImageField()
#     # 프로필 설명
#     profile_content = models.TextField(max_length=256)
#     # 타 사이트 아이디1
#     sns_username = models.EmailField(max_length=50)
#     # 타 사이트 아이디2
#     # another_id2 = models.CharField(max_length=50)
#     # 닉네임
#     nickname = models.CharField(max_length=30)
#     # 아이디 타입 (로그인시 구분)
#     id_type = models.CharField(max_length=30)





