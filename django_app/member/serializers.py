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
            # 'id_type',
            'img_profile',
            'password',
            # 'password2',
        )
