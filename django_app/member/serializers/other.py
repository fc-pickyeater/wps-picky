from rest_framework import serializers
from rest_framework.authtoken.models import Token

from member.models import PickyUser


__all__ = (
    'PickyUserSerializer',
)


class PickyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickyUser
        fields = (
            'pk',
            'email',
            'nickname',
            'content',
            'img_profile',
            'password',
            'id_type',
            # 아래는 확인을 위한 임시 필드 8/10 joe
            'created',
            'modified',
        )

    # API 리턴에 토큰 키, 값을 추가해주는 함수. 확인을 위해 추가 8/13 joe
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        token, _ = Token.objects.get_or_create(user=instance)
        ret['token'] = token.key
        return ret


# PickyUserSerializer로 통합함. 삭제 예정 8/13 joe
# class PickyUserDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PickyUser
#         fields = (
#             'pk',
#             'email',
#             'nickname',
#             'content',
#             'img_profile',
#             'id_type',
#         )
