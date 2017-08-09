from rest_framework import filters
from rest_framework import generics

from recipe.models import Recipe
from recipe.pagination import RecipePagination
from recipe.serializers import RecipeSearchListSerializer


class RecipeSearchListView(generics.ListAPIView):
    serializer_class = RecipeSearchListSerializer
    queryset = Recipe.objects.all()
    pagination_class = RecipePagination
    # 검색필터 django_filter
    filter_backends = (filters.SearchFilter,)
    # 검색옵션과 검색할 대상 '='는 완전일치
    # 자세한 옵션은 SearchFilter 참고
    search_fields = ('=title', '=ingredient__name')




    # def get_queryset(self):
    #     queryset_list = RecipeIngredient.objects.all()
    #     query = self.request.GET.get("q")
    #     if query:
    #         queryset_list = list(queryset_list.filter(
    #             Q(ingre_name__icontains=query) |
    #             Q(recipe=Recipe.objects.filter(title__icontains=query))
    #
    #         ))
    #         return queryset_list
    #
    #
    #     else:
    #         raise ValueError('검색어를 입력하세요.')
