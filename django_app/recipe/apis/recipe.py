from rest_framework import generics
from rest_framework import permissions

from utils.permissions import ObjectIsRequestUser
from ..models import Recipe, RecipeTag, Tag
from ..serializers.recipe import RecipeSerializer, RecipeCreateSerializer, RecipeListSerializer

__all__ = (
    'MyRecipeListView',
    'RecipeListView',
    'RecipeDetailView',
    'RecipeModifyDelete',
    'RecipeCreateForFDS',
)


# 레시피 리스트 조회 ListViewAPIView 사용
# 레시피의 기본내용만 사용하는 RecipeListSerializer로 변경 8/9 joe
class RecipeListView(generics.ListAPIView):
    # serializer는 RecipeSerializer 사용
    serializer_class = RecipeListSerializer
    # Recipe의 object 가져옴
    queryset = Recipe.objects.all()


# 1개의 레시피와 레시피에 달려있는 레시피 스탭들을 보기위한 뷰
class RecipeDetailView(generics.RetrieveAPIView):
    # RecipeStep의 List를 출력하기위한 Serializer 사용
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


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


# FDS용 레시피 생성 8/9 joe, 태그 추가 기능 8/15 joe
class RecipeCreateForFDS(generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer

    # tag 추가 8/15 joe
    def perform_create(self, serializer):
        serializer.save(
                user=self.request.user,
        )
        # 사용자가 tag 필드에 입력한 값을 가지고 옴
        tag = serializer.initial_data.get('tag', '')
        # ','로 구분하여 리스트를 만듬
        tag_list = tag.split(',')
        # 리스트를 순회하며
        for tag in tag_list:
            # Tag 테이블에 기존데이터가 있는지 확인하여 없으면 생성(이때 빈칸이 있으면 삭제-strip)
            tags, _ = Tag.objects.get_or_create(content=tag.strip())
            # RecipeTag 데이블에 기존데이터가 있는지 확인하여 없으면 생성(위에서 만들어진 Tag object 사용)
            recipe_tag, _ = RecipeTag.objects.get_or_create(recipe=serializer.instance, tag=tags)
