from rest_framework import serializers

from member.models import PickyUser


__all__ = (
    'PickyUserSerializer',
    'PickyUserUpdateSerializer',
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


class PickyUserUpdateSerializer(serializers.ModelSerializer):
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
        read_only_fields = (
            'email',
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
