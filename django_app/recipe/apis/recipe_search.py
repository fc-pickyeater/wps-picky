from django.db.models import Q
from rest_framework import generics

from recipe.models import Recipe
from recipe.models import RecipeIngredient
from recipe.serializers import RecipeSearchListSerializer


class RecipeSearchListView(generics.ListAPIView):
    serializer_class = RecipeSearchListSerializer

    def get_queryset(self):
        queryset_list = RecipeIngredient.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = list(queryset_list.filter(
                Q(ingre_name__icontains=query) |
                Q(recipe=Recipe.objects.filter(title__icontains=query))

            ))
            return queryset_list
        else:
            raise ValueError('검색어를 입력하세요.')
