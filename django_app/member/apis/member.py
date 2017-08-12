from rest_framework import generics
from rest_framework.authtoken.models import Token

from ..serializers.update import PickyUserUpdateSerializer
from ..serializers import (
    PickyUserSerializer,
    PickyUserDetailSerializer,
    PickyUserTokenSerializer,
)
from ..serializers import PickyUserCreateSerializer
from ..models import PickyUser

__all__ = (
    'PickyUserList',
    'PickyUserDetail',
    'PickyUserCreate',
    'PickyUserDelete',
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
    serializer_class = PickyUserDetailSerializer


# 회원정보 부분 업데이트 8/12 joe
class PickyUserUpdate(generics.UpdateAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserUpdateSerializer
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated, ObjectIsRequestUser,)

    # 회원정보 부분 업데이트하는 함수 8/12 joe
    # 키 조차 없는 값이 있어도 키에러 나지 않음. (partial_update)
    # 입력된 데이터 검증은 시리얼라이져에서 해줌
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


# 정상 작동함 8/10 joe
class PickyUserCreate(generics.CreateAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserCreateSerializer


class PickyUserDelete(generics.DestroyAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserSerializer


# 쿼리셋을 get으로 수정
class PickyUserLogout(generics.DestroyAPIView):
    queryset = Token.objects.all()
    serializer_class = PickyUserTokenSerializer
