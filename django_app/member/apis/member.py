from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from ..serializers import PickyAuthTokenSerializer
from ..serializers import PickyUserSerializer, PickyUserDetailSerializer
from ..serializers import PickyUserCreateSerializer
from ..models import PickyUser

__all__ = (
    'PickyUserList',
    'PickyUserDetailUpdate',
    'PickyUserCreate',
    'PickyUserDelete',
    # 'PickyUserLogin',
)


# user list / test 용도 8/2 Joe
# postman, 배포환경에서 정상작동 확인 8/4 Joe
class PickyUserList(generics.ListAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserSerializer


# postman, 배포환경에서 GET만 정상작동 확인 8/4 Joe
class PickyUserDetailUpdate(generics.RetrieveUpdateAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserDetailSerializer


# postman, 배포환경에서 확인함. 데이터 생성은 되지만 password 저장되지않음 8/4 Joe
class PickyUserCreate(generics.CreateAPIView):
    # queryset = PickyUser.objects.all()
    serializer_class = PickyUserCreateSerializer


class PickyUserDelete(generics.DestroyAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserSerializer



# 필요없음... 8/7 Joe
# class PickyUserLogin(generics.GenericAPIView):
#     # authentication_classes = (SessionAuthentication, BasicAuthentication)
#     # permission_classes = (IsAuthenticated,)
#     serializer_class = PickyAuthTokenSerializer





