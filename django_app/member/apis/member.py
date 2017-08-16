from rest_framework import generics, status, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from utils.permissions import ObjectIsRequestUser
from ..serializers.update import PickyUserUpdateSerializer
from ..serializers import (
    PickyUserSerializer,
    PickyUserTokenSerializer,
)
from ..serializers import PickyUserCreateSerializer
from ..models import PickyUser

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
class PickyUserDetail(generics.RetrieveAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserSerializer
    permission_classes = (permissions.IsAuthenticated,)


# 회원정보 부분 업데이트 8/12 joe / user permission 만들어야할것 같음.
class PickyUserUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    PUT : 수정
    DELETE : 삭제
    """
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

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
    queryset = Token.objects.all()
    serializer_class = PickyUserTokenSerializer
