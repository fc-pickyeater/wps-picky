import six
from rest_framework import status
from rest_framework.exceptions import _get_error_details, APIException


# 기존 serializers.Validation을 오버라이딩
# 오류 메시지에 리스트 형식을 빼달라고 하여 오버라이딩 후 수정 - hong 8/16
class CustomValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ('찾을수 없습니다.')
    default_code = 'invalid'

    def __init__(self, detail, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect may errors together, so the
        # details should always be coerced to a list if not already.
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = detail

        self.detail = _get_error_details(detail, code)

    def __str__(self):
        return six.text_type(self.detail)
