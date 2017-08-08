from rest_framework import serializers

from member.models import PickyUser


__all__ = (
    'PickyUserSerializer',
    'PickyUserDetailSerializer',
    'PickyUserUpdateSerializer',
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
        )


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


class PickyUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickyUser
        fields = (
            'pk',
            'email',
            'nickname',
            'content',
            'img_profile',
        )
        read_only_fields = (
            # 'email',
        )
