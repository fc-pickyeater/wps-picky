from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from recipe.serializers import RecipeStepCreateSerializer
from utils.permissions import ObjectIsRequestUser
from ..models import Recipe
from ..models import RecipeStep
from ..serializers import RecipeStepListSerializer
from ..serializers.recipe import RecipeSerializer, RecipeCreateSerializer, RecipeListSerializer

__all__ = (
    'MyRecipeListView',
    'RecipeListView',
    'RecipeDetailView',
    'RecipeModifyDelete',
    # 'RecipeCreateView',
    'RecipeCreateForFDS',

    # recipestep.py로 이동 8/9 joe
    # 'RecipeStepCreateForFDS',
)


# 레시피 리스트 조회 ListViewAPIView 사용
# 레시피의 기본내용만 사용하는 RecipeListSerializer로 변경 8/9 joe
class RecipeListView(generics.ListAPIView):
    # serializer는 RecipeSerializer 사용
    serializer_class = RecipeListSerializer
    # Recipe의 object 가져옴
    queryset = Recipe.objects.all()


# 레시피 생성하는 API 테스트용으로 짠코드 - 8/7 hong
# RecipeCreateForFDS로 변경하여 적용 8/9 joe
# class RecipeCreateView(generics.CreateAPIView):
#     serializer_class = RecipeCreateSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# 1개의 레시피와 레시피에 달려있는 레시피 스탭들을 보기위한 뷰
class RecipeDetailView(generics.RetrieveAPIView):
    # RecipeStep의 List를 출력하기위한 Serializer 사용
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    # RecipeStep(Recipe에 ForeignKey)의 object들을
    # queryset으로 가져와서 recipe에 할당 후 리턴
    # def get_queryset(self):
    #     recipe = RecipeStep.objects.all()
    #     RecipeStep.objects.filter(recipe_id=recipe)
        # return recipe


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
    # 8/8 hong 주석추가
    # 로그인한 유저만 수정 삭제가 가능
    # 퍼미션 클래스는 IsAuthenticated와 커스텀 퍼미션 ObjectsIsRequestUser 사용
    permission_classes = (permissions.IsAuthenticated, ObjectIsRequestUser,)
    # RecipeSerializer 사용
    serializer_class = RecipeSerializer


# FDS용 레시피 생성 8/9 joe
class RecipeCreateForFDS(generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(
                user=self.request.user,
        )


# recipestep.py로 이동 8/9 joe
# 'RecipeStepCreateForFDS',
