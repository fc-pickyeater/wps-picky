from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions

from recipe.models import Recipe
from recipe.serializers.recipe import RecipeSerializer
from utils.permissions import ObjectIsRequestUser

__all__ = (
    'RecipeList',
    'RecipeModifyDelete',
)


# 8/1 승팔씀
class RecipeList(generics.ListCreateAPIView):
    """
    POST GET
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticated, ObjectIsRequestUser,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('title',)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeSerializer
        elif self.request.method == 'GET':
            return RecipeSerializer


# 8/1 승팔씀
class RecipeModifyDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    PATCH DELETE
    """
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticated, ObjectIsRequestUser,)
    serializer_class = RecipeSerializer
