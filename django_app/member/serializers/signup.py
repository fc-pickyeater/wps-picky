from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from ..models import PickyUser

__all__ = (
    'PickyUserCreateSerializer',
)


# PickyUser 생성
class PickyUserCreateSerializer(serializers.Serializer):
    img_profile = serializers.ImageField(
            max_length=None,
            use_url=True,
            required=False,
    )
    email = serializers.CharField(max_length=100)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    nickname = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=200, allow_null=True, required=False)

    # validate_[필드 이름] <- 함수 이름을 꼭! 이렇게지정해야 해당 필드를 검사함.
    def validate_email(self, email):
        if PickyUser.objects.filter(email=email).exists():
            d = {}
            d['result_code'] = 11
            d['error_msg'] = '다른 사용자가 사용 중인 email입니다.'
            raise serializers.ValidationError(d)
        else:
            try:
                validate_email(email)
            except ValidationError:
                d = {}
                d['result_code'] = 12
                d['error_msg'] = '유효한 이메일을 입력하세요.'
                raise serializers.ValidationError(d)
        return email

    def validate_nickname(self, nickname):
        if PickyUser.objects.filter(nickname=nickname).exists():
            d = {}
            d['result_code'] = 21
            d['error_msg'] = '다른 사용자가 사용 중인 Nickname입니다.'
            raise serializers.ValidationError(d)
        return nickname

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('입력된 패스워드가 일치하지 않습니다.')
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

