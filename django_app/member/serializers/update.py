from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from utils.exceptions import CustomValidationError

PickyUser = get_user_model()


class PickyUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickyUser
        # allow_null=True, required=False 할 필요없음(partial_update에서 알아서 걸러줌)
        fields = (
            'img_profile',
            'content',
            'password',
            'nickname',
            'password1',
            'password2',
        )
        read_only_fields = (
            'password',
        )
    # 모델에 없는 필드라서 재정의
    password1 = serializers.CharField(
        write_only=True,
        allow_null=True,
        required=False,
        allow_blank=True
    )
    password2 = serializers.CharField(
        write_only=True,
        allow_null=True,
        required=False,
        allow_blank=True
    )
    nickname = serializers.CharField(
        allow_null=True,
        required=False,
        allow_blank=True
    )

    # nickname 필드를 검사하는 함수 8/12 joe
    # 특정 필드만 검사하려면 validate_[특정필드이름] 으로 함수를 정의하면 됨

    # 비번은 2개의 필드를 검사해야되므로 따로 함수를 만들 수 없음 8/12 joe
    # iOS 요청대로 error 메세지 출력 형태 수정 8/16 joe
    def validate(self, data):
        d = dict()
        nickname = self.initial_data.get('nickname', None)
        password1 = self.initial_data.get('password1', None)
        password2 = self.initial_data.get('password2', None)
        old_password = self.initial_data.get('password', None)
        content = self.initial_data.get('content', None)
        img_profile = self.initial_data.get('img_profile', None)

        # nickname 체크
        # nickname이 중복된 경우
        # 닉네임 데이터가 있으면서 빈값이 아닌경우 (닉네임을 바꾸는 경우)
        if nickname and nickname != '':
            # 바꾸려는 닉네임 데이터가 현재 닉네임과 다른 경우
            if nickname != self.instance.nickname:
                if PickyUser.objects.filter(nickname=nickname).exists():
                    d['nickname_exists'] = '이미 사용 중인 Nickname입니다.'
                    raise CustomValidationError(d)
        # nickname을 바꾸지 않은 경우
        else:
            data['nickname'] = self.instance.nickname

        # content 체크
        # content에 값이 없으면 기존 값으로 저장
        if content == '' or content is None:
            data['content'] = self.instance.content

        # img_profile 체크
        # img_profile에 값이 없으면 기존 값으로 저장
        if img_profile == '' or img_profile is None:
            data['img_profile'] = self.instance.img_profile

        # 비번 체크
        # password 필드 중 하나라도 데이터가 있는 경우(패스워드변경을 시도하는 경우)
        if password1 or password2 or old_password:
            # 기존 비번의 값이 없을 경우
            if not old_password or old_password == '':
                d['empty_old_password'] = '기존 패스워드를 입력해주세요.'
                raise CustomValidationError(d)
            # 기존 비번이 맞지 않을 경우
            elif not self.instance.check_password(old_password):
                d['old_password_error'] = '기존 패스워드가 맞지 않습니다.'
                raise CustomValidationError(d)
            # 새로운 비번이 하나만 비어있을 경우
            elif (not password1 and password2) or password1 == '':
                d['empty_password1'] = 'password1을 입력해주세요.'
                raise CustomValidationError(d)
            elif (password1 and not password2)or password2 == '':
                d['empty_password2'] = 'password2를 입력해주세요.'
                raise CustomValidationError(d)
            # 비번이 4글자보다 적으면 에러 발생
            elif len(password1) < 4 or len(password2) < 4:
                d['too_short_password'] = '패스워드는 최소 4글자 이상이어야 합니다.'
                raise CustomValidationError(d)
            # 입력된 비번이 다르면 에러 발생
            elif password1 != password2:
                d['passwords_not_match'] = '입력된 패스워드가 일치하지 않습니다'
                raise CustomValidationError(d)
        # 위 조건들을 통과하면 입력된 비번을 해시해서 저장
            else:
                self.instance.set_password(password1)
        return data

    # API 리턴에 키, 값을 추가해주는 함수
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        nickname = instance.nickname
        email = instance.email
        token, _ = Token.objects.get_or_create(user=instance)
        ret['nickname'] = nickname
        ret['token'] = token.key
        ret['email'] = email
        return ret
