from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from utils.exceptions import CustomValidationError

PickyUser = get_user_model()

__all__ = (
    'PickyUserCreateSerializer',
)


# PickyUser 생성
class PickyUserCreateSerializer(serializers.Serializer):
    img_profile = serializers.ImageField(
            max_length=None,
            use_url=True,
            required=False,
            allow_null=True,
    )
    email = serializers.CharField(max_length=100, allow_null=True, required=False, allow_blank=True)
    password1 = serializers.CharField(write_only=True, allow_null=True, required=False, allow_blank=True)
    password2 = serializers.CharField(write_only=True, allow_null=True, required=False, allow_blank=True)
    nickname = serializers.CharField(max_length=100, allow_null=True, required=False, allow_blank=True)
    content = serializers.CharField(max_length=200, allow_null=True, required=False, allow_blank=True)

    # iOS 요청대로 error 메세지 출력 형태 수정 8/16 joe
    def validate(self, data):
        d = dict()
        email = data.get('email', None)
        nickname = data.get('nickname', None)
        password1 = data.get('password1', None)
        password2 = data.get('password2', None)
        # email 필드 검증
        if email is None or email == '':
            d['email_empty'] = 'email을 입력해주세요.'
            raise CustomValidationError(d)
        if PickyUser.objects.filter(email=email).exists():
            d['email_error'] = '다른 사용자가 사용 중인 email입니다.'
            raise CustomValidationError(d)
        else:
            try:
                validate_email(email)
            except ValidationError:
                d['email_invalid'] = '유효한 이메일을 입력하세요.'
                raise CustomValidationError(d)
        # nickname 필드 검증
        if nickname is None or nickname == '':
            d['nickname_empty'] = 'nickname을 입력해주세요.'
            raise CustomValidationError(d)
        if PickyUser.objects.filter(nickname=nickname).exists():
            d['nickname_error'] = '다른 사용자가 사용 중인 Nickname입니다.'
            raise CustomValidationError(d)
        # 입력된 password 필드 검증
        if (not password1 and not password2) or (password2 is None and password1 is None):
            d['empty_passwords'] = 'password1과 password2를 입력해주세요.'
            raise CustomValidationError(d)
        elif (password1 and not password2) or password2 is None:
            d['empty_password2'] = 'password2를 입력해주세요.'
            raise CustomValidationError(d)
        elif (not password1 and password2) or password1 is None:
            d['empty_password1'] = 'password1을 입력해주세요.'
            raise CustomValidationError(d)
        elif password1 != password2:
            d['passwords_not_match'] = '입력된 패스워드가 일치하지 않습니다.'
            raise CustomValidationError(d)
        elif len(password1) < 4:
            d['too_short_password'] = '패스워드는 최소 4글자 이상이어야 합니다.'
            raise CustomValidationError(d)
        return data

    def create(self, *args, **kwargs):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password1')
        nickname = self.validated_data.get('nickname')
        img_profile = self.validated_data.get('img_profile')
        content = self.validated_data.get('content')
        user = PickyUser.objects.create_user(
            email=email,
            password=password,
            nickname=nickname,
            img_profile=img_profile,
            content=content,
        )
        return user

    # API 리턴에 키, 값을 추가해주는 함수
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        token, _ = Token.objects.get_or_create(user=instance)
        ret['token'] = token.key
        return ret
