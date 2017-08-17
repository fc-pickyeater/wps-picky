from rest_framework import filters
from rest_framework import generics

from recipe.models import Recipe
from recipe.pagination import RecipePagination
from recipe.serializers import RecipeSearchListSerializer

__all__ = (
    'RecipeSearchListView',
    'RecipeTagSearchView'
)


# 전체 레시피 검색
# 전체 레시피에서 ?search=parameter에 대한 title,ingredient,tag를 검색
class RecipeSearchListView(generics.ListAPIView):
    serializer_class = RecipeSearchListSerializer
    queryset = Recipe.objects.all()
    pagination_class = RecipePagination
    # 검색필터 django_filter
    filter_backends = (filters.SearchFilter,)
    # 검색옵션과 검색할 대상 '='는 완전일치
    # 자세한 옵션은 SearchFilter 참고
    search_fields = ('=title', '=ingredient__name', '=tag__content')


# 전체 레시피 검색
# 전체 레시피에서 ?search=parameter에 대한 tag만 검색
class RecipeTagSearchView(generics.ListAPIView):
    serializer_class = RecipeSearchListSerializer
    queryset = Recipe.objects.all()
    pagination_class = RecipePagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=tag__content',)
