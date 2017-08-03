from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions

from ingredient.models import Ingredient
from ingredient.serializers.ingredient import IngredientSerializer
from utils.permissions import ObjectIsRequestUser

__all__ = (
    'IngredientSearchList',
    'IngredientModifyDelete',
)


# ingredient search and list post요청시 생성 get요청시 list postman 확인 - hong 8/1
class IngredientSearchList(generics.ListCreateAPIView):
    """
    POST GET
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, ObjectIsRequestUser,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return IngredientSerializer
        elif self.request.method == 'GET':
            return IngredientSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ingredient modify and delete patch요청시 수정 delete요청시 삭제 postman 확인 - hong 8/1
class IngredientModifyDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    PATCH DELETE
    """
    queryset = Ingredient.objects.all()
    permission_classes = (permissions.IsAuthenticated, ObjectIsRequestUser,)
    serializer_class = IngredientSerializer

    # permission_classes = (
    #     permissions.IsAuthenticatedOrReadOnly,
    #     ObjectIsRequestUser,
    # )
