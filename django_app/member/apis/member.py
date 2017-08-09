from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

# from ..serializers import PickyAuthTokenSerializer
from rest_framework.response import Response

from ..serializers import (PickyUserSerializer, PickyUserDetailSerializer, PickyUserTokenSerializer,
                           PickyUserUpdateSerializer)
from ..serializers import PickyUserCreateSerializer
from ..models import PickyUser

__all__ = (
    'PickyUserList',
    'PickyUserDetail',
    'PickyUserCreate',
    'PickyUserDelete',
    # 'PickyUserLogin',
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


# detail에서 분리. email 수정할 수 없게 바꿔야함 8/7 Joe
class PickyUserUpdate(generics.UpdateAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserUpdateSerializer

    def perform_create(self, serializer):
        serializer.save()


# postman에서 img_profile 값이 null로 반환됨. DB에는 저장됨. 배포환경에서 500에러 8/7 Joe
class PickyUserCreate(generics.CreateAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserCreateSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer_class = AuthTokenSerializer
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data['user']
    #     token, created = Token.objects.get_or_create(user=user)
    #     return Response({'token': token.key})


class PickyUserDelete(generics.DestroyAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserSerializer


# 쿼리셋을 get으로 수정
class PickyUserLogout(generics.DestroyAPIView):
    queryset = Token.objects.all()
    serializer_class = PickyUserTokenSerializer


# 필요없음... 8/7 Joe
# class PickyUserLogin(generics.GenericAPIView):
#     # authentication_classes = (SessionAuthentication, BasicAuthentication)
#     # permission_classes = (IsAuthenticated,)
#     serializer_class = PickyAuthTokenSerializer





