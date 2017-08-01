from rest_framework import filters
from rest_framework import generics

from recipe.models import Recipe
from recipe.serializers.recipelist import RecipeSerializer

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
    serializer_class = RecipeSerializer