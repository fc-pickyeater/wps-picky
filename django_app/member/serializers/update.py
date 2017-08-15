from rest_framework import serializers
from rest_framework.authtoken.models import Token

from member.models import PickyUser


class PickyUserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PickyUser
        # allow_null=True, required=False 할 필요없음(partial_update에서 알아서 걸러줌)
        fields = (
            'img_profile',
            'nickname',
            'content',
            'password',
        )
        read_only_fields = (
            'password',
        )
        # 모델에 없는 필드라서 재정의
        password1 = serializers.CharField(
            write_only=True,
        )
        password2 = serializers.CharField(
            write_only=True,
        )

    # nickname 필드를 검사하는 함수 8/12 joe
    # 특정 필드만 검사하려면 validate_[특정필드이름] 으로 함수를 정의하면 됨
    def validate_nickname(self, nickname):
        if PickyUser.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError('이미 사용 중인 Nickname입니다.')
        return nickname

    # 비번은 2개의 필드를 검사해야되므로 따로 함수를 만들 수 없음 8/12 joe
    def validate(self, data):
        password1 = self.initial_data.get('password1', None)
        password2 = self.initial_data.get('password2', None)
        old_password = self.initial_data.get('password', None)
        # 비번 키가 없을 경우 data 리턴하고 종료 (비번을 안바꾸는 경우)
        if password1 is None and password2 is None:
            return data
        # 기존 비번을 받아서 체크
        if not self.instance.check_password(old_password):
            raise serializers.ValidationError('기존 패스워드가 맞지 않습니다.')
        # 비번이 4글자보다 적으면 에러 발생
        if len(self.initial_data['password1']) < 4:
            d = dict()
            d['error_msg'] = '패스워드는 최소 4글자 이상이어야 합니다.'
            d['result_code'] = 31
            raise serializers.ValidationError(d)
        # 입력된 비번이 다르면 에러 발생
        if password1 != password2:
            d = dict()
            d['error_msg'] = '입력된 패스워드가 일치하지 않습니다'
            d['result_code'] = 33
            raise serializers.ValidationError(d)
        # 위 조건들을 통과하면 입력된 비번을 해시해서 저장
        self.instance.set_password(password1)
        return data

    # API 리턴에 키, 값을 추가해주는 함수
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        email = instance.email
        token, _ = Token.objects.get_or_create(user=instance)
        ret['token'] = token.key
        ret['email'] = email
        return ret
