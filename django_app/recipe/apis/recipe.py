from rest_framework import generics
from rest_framework import permissions

from recipe.models import Recipe
from recipe.models import RecipeStep
from recipe.serializers import RecipeStepListSerializer
from recipe.serializers.recipe import RecipeSerializer
from utils.permissions import ObjectIsRequestRecipe, ObjectIsRequestUser




__all__ = (
    'MyRecipeListView',
    'RecipeListView',
    'RecipeDetailView',
    'RecipeModifyDelete',
)


# 8/1 승팔씀
class RecipeListView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


# 레시피에 달려있는 레시피 스탭들을 보기위한 시리얼라이저
class RecipeDetailView(generics.RetrieveAPIView):
    serializer_class = RecipeStepListSerializer

    def get_queryset(self):
        recipe = RecipeStep.objects.all()
        print(recipe)
        return recipe#RecipeStep.objects.filter(recipe_id=recipe)


# 8/3 hong 로그인 한 유저가 자기가 쓴 레시피 리스트를 볼 수 있게 만들었음
class MyRecipeListView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = (
        permissions.IsAuthenticated, ObjectIsRequestUser,
    )

    def get_queryset(self):
        user = self.request.user
        return user.recipe_set.filter(user_id=user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer


# 8/1 승팔씀
class RecipeModifyDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    PATCH DELETE
    """
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticated, ObjectIsRequestRecipe,)
    serializer_class = RecipeSerializer
