from rest_framework import serializers

from member.models import PickyUser


__all__ = (
    'PickyUserSerializer',
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
        )
