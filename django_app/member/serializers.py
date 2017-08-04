from rest_framework import serializers
from .models import PickyUser


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


# PickyUser 생성
class PickyUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickyUser
        fields = (
            'pk',
            'email',
            'nickname',
            'content',
            'img_profile',
        )
        # 전송되지만 JSON에 보이지않을 필드 지정
        write_only_fields = (
            'password',
        )
