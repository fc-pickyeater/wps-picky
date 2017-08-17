from django.contrib.auth import get_user_model
from utils.permissions import ObjectIsMe

from rest_framework import generics, permissions
from rest_framework.response import Response
from ..serializers import (
    PickyUserSerializer,
    PickyUserCreateSerializer,
    PickyUserUpdateSerializer
)

PickyUser = get_user_model()

__all__ = (
    'PickyUserList',
    'PickyUserDetail',
    'PickyUserCreate',
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
    PATCH : 수정
    DELETE : 삭제
    """
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated, ObjectIsMe)

    def delete(self, request, *args, **kwargs):
        d = dict()
        d['result'] = '탈되되었습니다.'
        self.destroy(request, *args, **kwargs)
        return Response(d)


# 유저 생성(회원가입) 정상 작동함 8/10 joe
class PickyUserCreate(generics.CreateAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserCreateSerializer


class PickyUserLogout(generics.DestroyAPIView):
    queryset = PickyUser.objects.all()
    permission_classes = (permissions.IsAuthenticated, ObjectIsMe)

    def post(self, request, *args, **kwargs):
        d = dict()
        d['result'] = '로그아웃 되었습니다.'
        request.user.auth_token.delete()
        return Response(d)
