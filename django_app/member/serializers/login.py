from django.contrib.auth import get_user_model
from rest_framework import generics, serializers
from rest_framework.authtoken.models import Token

PickyUser = get_user_model()


class FacebookLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickyUser
        fields = (
            'img_profile',
            'email',
            'nickname',
        )

    # API 리턴에 키, 값을 추가해주는 함수
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        token, _ = Token.objects.get_or_create(user=instance)
        ret['token'] = token.key
        ret['img_profile'] = instance.img_profile.name
        return ret
