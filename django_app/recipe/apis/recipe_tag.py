from rest_framework import generics

from recipe.models import RecipeTag, Recipe, Tag
from recipe.serializers.recipe_tag import RecipeTagCreateSerializer
from utils import permissions


__all__ = (
    'RecipeTagCreate',
)


# 이방법이 아닌거같음... 8/14 joe
class RecipeTagCreate(generics.CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = RecipeTagCreateSerializer
    # permission_classes = (
    #     permissions.IsAuthenticated,
    # )

    # 생성 함수
    def perform_create(self, serializer):
        recipe_pk = self.kwargs['pk']
        serializer.save(
            user=self.request.user,
            recipe=Recipe.objects.get(pk=recipe_pk)
        )
