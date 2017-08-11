from rest_framework import serializers

from member.models import PickyUser


__all__ = (
    'PickyUserSerializer',
    # 'PickyUserUpdateSerializer',
    'PickyUserDetailSerializer',
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
            # 아래는 확인을 위한 임시 필드 8/10 joe
            'created',
            'modified',
        )


# class PickyUserUpdateSerializer(serializers.ModelSerializer):
#     password1 = serializers.CharField(
#             write_only=True,
#             required=False,
#             allow_null=True
#     )
#     password2 = serializers.CharField(
#             write_only=True,
#             required=False,
#             allow_null=True
#     )
#
#     class Meta:
#         model = PickyUser
#         fields = (
#             'pk',
#             'email',
#             'nickname',
#             'content',
#             'img_profile',
#             'password',
#             # 'password1',
#             # 'password2',
#         )
#         read_only_fields = (
#             'email',
#         )
#
#     def save(self, **kwargs):
#         if self.password1 != self.password2:
#             raise serializers.ValidationError('입력된 패스워드가 일치하지 않습니다.')
#         super().save(**kwargs)


class PickyUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickyUser
        fields = (
            'pk',
            'email',
            'nickname',
            'content',
            'img_profile',
            'id_type',
        )
