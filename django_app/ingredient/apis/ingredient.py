from rest_framework import filters
from rest_framework import generics

from ingredient.models import Ingredient
from ingredient.serializers.ingredient import IngredientSerializer

__all__ = (
    'IngredientSearchList',
    'IngredientModifyDelete',
)


class IngredientSearchList(generics.ListCreateAPIView):
    """
    POST GET
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return IngredientSerializer
        elif self.request.method == 'GET':
            return IngredientSerializer


class IngredientModifyDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    PATCH DELETE
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    # permission_classes = (
    #     permissions.IsAuthenticatedOrReadOnly,
    #     ObjectIsRequestUser,
    # )
