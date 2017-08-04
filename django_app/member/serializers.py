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
# ImageField override -> 배포후 테스트필요. 로컬에서 작동됨. 8/4 Joe
class PickyUserCreateSerializer(serializers.ModelSerializer):
    img_profile = Base64ImageField(
            max_length=None,
            use_url=True,
    )

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


# 배포 후 이미지를 저장하기 위해 조사한 예시 8/4 Joe
# 배포후 테스트필요. 로컬에서 작동됨. 8/4 Joe
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension
