from rest_framework import generics

from ..serializers import PickyUserSerializer, PickyUserCreateSerializer, PickyUserDetailSerializer
from ..models import PickyUser

__all__ = (
    'PickyUserList',
    'PickyUserDetailUpdate',
    'PickyUserCreate',
    'PickyUserDelete',
)


# user list / test 용도 8/2 Joe
class PickyUserList(generics.ListAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserSerializer


class PickyUserDetailUpdate(generics.RetrieveUpdateAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserDetailSerializer


class PickyUserCreate(generics.CreateAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserCreateSerializer


class PickyUserDelete(generics.DestroyAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserSerializer
