from rest_framework import generics

from ..serializers import PickyUserSerializer
from ..models import PickyUser

__all__ = (
    'PickyUserList',
)


# user list / test 용도 8/2 Joe
class PickyUserList(generics.ListAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserSerializer
