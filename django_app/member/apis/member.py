from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from utils.permissions import ObjectIsMe
from ..serializers import PickyUserCreateSerializer
from ..serializers import (
    PickyUserSerializer,
)
from ..serializers.update import PickyUserUpdateSerializer

PickyUser = get_user_model()

__all__ = (
    'PickyUserList',
    'PickyUserDetail',
    'PickyUserCreate',
    # 'PickyUserDelete',
    'PickyUserLogout',
    'PickyUserUpdate',
)


# user list / test 용도 8/2 Joe
# postman, 배포환경에서 정상작동 확인 8/4 Joe
class PickyUserList(generics.ListAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserSerializer


# postman, 배포환경에서 정상작동 확인 8/7 Joe
# permissions ObjectIsMe 추가 8/17 hong
class PickyUserDetail(generics.RetrieveAPIView):
    serializer_class = PickyUserSerializer
    permission_classes = (permissions.IsAuthenticated, ObjectIsMe)
    queryset = PickyUser.objects.all()


# 회원정보 부분 업데이트 8/12 joe / user permission 만들어야할것 같음.
# permissions ObjectIsMe 추가 8/17 hong
class PickyUserUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    PUT : 수정
    DELETE : 삭제
    """
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated, ObjectIsMe)

    # 회원정보 부분 업데이트하는 함수 8/12 joe
    # 키 조차 없는 값이 있어도 키에러 나지 않음. (partial_update)
    # 입력된 데이터 검증은 시리얼라이져에서 해줌
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        d = dict()
        d['result'] = '탈되되었습니다.'
        self.destroy(request, *args, **kwargs)
        return Response(d, status=status.HTTP_202_ACCEPTED)


# 유저 생성(회원가입) 정상 작동함 8/10 joe
class PickyUserCreate(generics.CreateAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserCreateSerializer


# 안됨.... 8/13 joe
class PickyUserLogout(generics.DestroyAPIView):
    queryset = PickyUser.objects.all()
    permission_classes = (permissions.IsAuthenticated, ObjectIsMe)

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response("로그아웃 되었습니다.")
