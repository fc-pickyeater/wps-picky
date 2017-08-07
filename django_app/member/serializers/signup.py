# 배포 후 이미지를 저장하기 위해 조사한 예시 8/4 Joe
# 배포후 테스트필요. 로컬에서 작동됨. 8/4 Joe
from rest_framework import serializers

from ..models import PickyUser


__all__ = (
    'PickyUserCreateSerializer',
)


# PickyUser 생성
# ImageField override -> 배포환경, 로컬에서 작동됨. 8/7 Joe
# class Base64ImageField(serializers.ImageField):
#
#     def to_internal_value(self, data):
#         from django.core.files.base import ContentFile
#         import base64
#         import six
#         import uuid
#
#         # Check if this is a base64 string
#         if isinstance(data, six.string_types):
#             # Check if the base64 string is in the "data:" format
#             if 'data:' in data and ';base64,' in data:
#                 # Break out the header from the base64 content
#                 header, data = data.split(';base64,')
#
#             # Try to decode the file. Return validation error if it fails.
#             try:
#                 decoded_file = base64.b64decode(data)
#             except TypeError:
#                 self.fail('invalid_image')
#
#             # Generate file name:
#             file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
#             # Get the file name extension:
#             file_extension = self.get_file_extension(file_name, decoded_file)
#
#             complete_file_name = "%s.%s" % (file_name, file_extension,)
#
#             data = ContentFile(decoded_file, name=complete_file_name)
#
#         return super(Base64ImageField, self).to_internal_value(data)
#
#     def get_file_extension(self, file_name, decoded_file):
#         import imghdr
#
#         extension = imghdr.what(file_name, decoded_file)
#         extension = "jpg" if extension == "jpeg" else extension
#
#         return extension


# PickyUser 생성
# ImageField 로컬에서 작동됨. 8/7 Joe
class PickyUserCreateSerializer(serializers.Serializer):
    img_profile = serializers.ImageField(
            # max_length=None,
            # use_url=True,
    )
    username = serializers.CharField(max_length=100)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    nickname = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=200)

    def validate_username(self, username):
        if PickyUser.objects.filter(email=username).exists():
            raise serializers.ValidationError('다른 사용자가 사용 중인 email입니다.')
        return username

    def validate_nickname(self, nickname):
        if PickyUser.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError('다른 사용자가 사용 중인 Nickname입니다.')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('입력된 패스워드가 일치하지 않습니다.')
        return data

    def save(self, *args, **kwargs):
        username = self.validated_data.get('username')
        password = self.validated_data.get('password1')
        nickname = self.validated_data.get('nickname')
        img_profile = self.validated_data.get('img_profile')
        content = self.validated_data.get('content')
        user = PickyUser.objects.create_user(
                email=username,
                password=password,
                nickname=nickname,
                img_profile=img_profile,
                content=content,
        )
        return user
