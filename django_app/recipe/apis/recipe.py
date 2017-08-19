from rest_framework import generics
from rest_framework import permissions

from utils.permissions import ObjectIsRequestUser
from ..models import Recipe, RecipeTag, Tag
from ..serializers.recipe import RecipeSerializer, RecipeCreateSerializer, RecipeListSerializer

__all__ = (
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

    def perform_update(self, serializer):
        old_tag = RecipeTag.objects.filter(recipe_id=self.kwargs['pk'])
        old_tag.delete()
        # 사용자가 tag 필드에 입력한 값을 가지고 옴
        tag = serializer.initial_data.get('tag', '')
        # ','로 구분하여 리스트를 만듬
        tag_list = tag.split(',')
        # 리스트를 순회하며
        for tag in tag_list:
            # 리스트에 있는 값의 앞뒤 공백제거한 뒤, 내부의 공백은 '_'로 치환
            cleaned_tag = tag.strip().replace(' ', '_')
            # Tag 테이블에 기존데이터가 있는지 확인하여 없으면 생성(이때 빈칸이 있으면 삭제-strip)
            tags, _ = Tag.objects.get_or_create(content=cleaned_tag)
            # RecipeTag 데이블에 기존데이터가 있는지 확인하여 없으면 생성(위에서 만들어진 Tag object 사용)
            recipe_tag, _ = RecipeTag.objects.get_or_create(recipe=serializer.instance, tag=tags)

        serializer.save(
            user=self.request.user,
        )


# FDS용 레시피 생성 8/9 joe, 태그 추가 기능 8/15 joe
class RecipeCreateForFDS(generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

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
            # 리스트에 있는 값의 앞뒤 공백제거한 뒤, 내부의 공백은 '_'로 치환
            cleaned_tag = tag.strip().replace(' ', '_')
            # Tag 테이블에 기존데이터가 있는지 확인하여 없으면 생성(이때 빈칸이 있으면 삭제-strip)
            tags, _ = Tag.objects.get_or_create(content=cleaned_tag)
            # RecipeTag 데이블에 기존데이터가 있는지 확인하여 없으면 생성(위에서 만들어진 Tag object 사용)
            recipe_tag, _ = RecipeTag.objects.get_or_create(recipe=serializer.instance, tag=tags)

