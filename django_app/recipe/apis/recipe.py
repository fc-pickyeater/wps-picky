from rest_framework import generics
from rest_framework import permissions

from recipe.serializers import RecipeStepCreateSerializer
from ..models import Recipe
from ..models import RecipeStep
from ..serializers import RecipeStepListSerializer
from ..serializers.recipe import RecipeSerializer, RecipeCreateSerializer
from utils.permissions import ObjectIsRequestRecipe, ObjectIsRequestUser


__all__ = (
    'MyRecipeListView',
    'RecipeListView',
    'RecipeDetailView',
    'RecipeModifyDelete',
    'RecipeCreateForFDS',
    'RecipeStepCreateForFDS',
)


# 레시피 리스트 조회 ListViewAPIView 사용
class RecipeListView(generics.ListAPIView):
    # serializer는 RecipeSerializer 사용
    serializer_class = RecipeSerializer
    # Recipe의 object 가져옴
    queryset = Recipe.objects.all()


# 레시피에 달려있는 레시피 스탭들을 보기위한 시리얼라이저
class RecipeDetailView(generics.RetrieveAPIView):
    # RecipeStep의 List를 출력하기위한 Serializer 사용
    serializer_class = RecipeStepListSerializer

    # RecipeStep(Recipe에 ForeignKey)의 object들을
    # queryset으로 가져와서 recipe에 할당 후 리턴
    def get_queryset(self):
        recipe = RecipeStep.objects.all()
        # RecipeStep.objects.filter(recipe_id=recipe)
        return recipe


# 마이페이지에서 자신이 작성한 Recipe 목록 확인
class MyRecipeListView(generics.ListAPIView):
    # RecipeSerializer 사용
    serializer_class = RecipeSerializer
    # IsAuthenticated 클래스와 커스텀 퍼미션 ObjectIsRequestUser 사용
    permission_classes = (
        permissions.IsAuthenticated, ObjectIsRequestUser,
    )

    def get_queryset(self):
        user = self.request.user
        return user.recipe_set.filter(user_id=user)
        # return user.recipe_set.all()

    # method 확인, 필요한지... 8/9 joe
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer


# Recipe 수정 삭제
class RecipeModifyDelete(generics.RetrieveUpdateDestroyAPIView):
    # Recipe의 object 가져옴
    queryset = Recipe.objects.all()
    # 퍼미션 클래스는 IsAuthenticated와 커스텀 퍼미션 ObjectsIsRequestRecipe 사용
    permission_classes = (permissions.IsAuthenticated, ObjectIsRequestRecipe,)
    # RecipeSerializer 사용
    serializer_class = RecipeSerializer


class RecipeCreateForFDS(generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecipeStepCreateForFDS(generics.CreateAPIView):
    queryset = RecipeStep.objects.all()
    serializer_class = RecipeStepCreateSerializer

    # def get_queryset(self):
    #     recipe = self.request.data['recipe']
    #     return RecipeStep.objects.filter(recipe=recipe)

    # def perform_create(self, serializer):
    #     serializer.save(recipe=self.request.data['recipe'])





