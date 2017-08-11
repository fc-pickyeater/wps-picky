from rest_framework import status
from rest_framework.exceptions import ValidationError, _get_error_details, APIException, _get_codes
from django.utils import six

from rest_framework.views import exception_handler

# 작동확인 필요 8/11 joe
class EmailExistError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = '중복'
    default_code = 'invalid'
    key = 'status_code'

    def __init__(self, detail, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect may errors together, so the
        # details should always be coerced to a list if not already.
        # if not isinstance(detail, dict) and not isinstance(detail, list):
            # ret = {self.key: self.detail}
            # detail = detail

        self.detail = _get_error_details(detail, code)

    def __str__(self):
        ret = {self.key: self.status_code}
        return ret
        # return six.text_type(self.detail)

    # def get_codes(self):
    #     """
    #     Return only the code part of the error details.
    #
    #     Eg. {"name": ["required"]}
    #     """
    #     return _get_codes(self.detail)


# def custom_exception_handler(exc, context):
#     # Call REST framework's default exception handler first,
#     # to get the standard error response.
#     response = exception_handler(exc, context)
#
#     # Now add the HTTP status code to the response.
#     if response is not None:
#         response.data['status_code'] = response.status_code
#
#     return response
