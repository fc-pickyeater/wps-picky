from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from utils.exceptions import CustomValidationError

__all__ = (
    'PickyAuthTokenSerializer',
    'PickyUserTokenSerializer',
)


class PickyUserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = (
            'user_id',
            'key',
        )


# iOS 요청대로 error 메세지 출력 형태 수정 8/16 joe
class PickyAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(allow_null=True, required=False)
    password = serializers.CharField(allow_null=True, required=False, style={'input_type': 'password'})

    def validate(self, attrs):
        d = dict()
        email = attrs.get('email', None)
        password = attrs.get('password', None)
        # email, password가 비어있는 경우를 걸러냄
        if (email == '' and password == '') or (password is None and email is None):
            d['empty_error'] = 'email과 password를 입력해주세요.'
            raise CustomValidationError(d, code='authorization')
        elif (email and password == '') or password is None:
            d['empty_password'] = 'password를 입력해주세요.'
            raise CustomValidationError(d, code='authorization')
        elif (email == '' and password) or email is None:
            d['empty_email'] = 'email을 입력해주세요.'
            raise CustomValidationError(d, code='authorization')
        # email, password가 모두 입력되었을 경우
        else:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    d['activation_error'] = '활성화되지 않은 계정입니다.'
                    raise CustomValidationError(d, code='authorization')
            else:
                d['login_error'] = 'email 또는 비밀번호가 맞지 않습니다.'
                raise CustomValidationError(d, code='authorization')

        attrs['user'] = user
        return attrs
