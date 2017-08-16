# 경로 : utils 내 exception 폴더 생성 후 아래 코드 붙여넣기
# status code 삽입
from rest_framework.views import exception_handler


# 반환되는 JSON에 status_code를 같이 보내줌.
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response
