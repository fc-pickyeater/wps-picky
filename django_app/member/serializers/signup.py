# 배포 후 이미지를 저장하기 위해 조사한 예시 8/4 Joe
# 배포후 테스트필요. 로컬에서 작동됨. 8/4 Joe
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

    def validated_email(self, email):
        # 이메일 중복 체크를 피하기위해 임시로 만든 코드
        PickyUser.objects.filter(email=email).delete()

        if PickyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('다른 사용자가 사용 중인 email입니다.')
        elif validate_email(email):
            raise serializers.ValidationError('유효한 이메일 주소를 입력하십시오.')
        return email

    def validate_nickname(self, nickname):
        if PickyUser.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError('다른 사용자가 사용 중인 Nickname입니다.')
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
