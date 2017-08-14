from django.db import models

from ingredient.models import Ingredient
from ..models import Recipe

__all__ = (
    'RecipeIngredient',
    # 'Tag',
    # 'RecipeTag',
)


class RecipeIngredient(models.Model):
    # 레시피
    recipe = models.ForeignKey(Recipe)
    # 재료
    ingredient = models.ForeignKey(Ingredient)
    # 구분
    type = models.CharField(max_length=30)
    # 갯수
    amount = models.CharField(max_length=30)
    # 재료이름
    ingre_name = models.CharField(max_length=30)

#
# class Tag(models.Model):
#     content = models.CharField(max_length=20)
#     url = models.CharField(max_length=200, default='tag_search_url')
#
#     def tag_search_url(self):
#         tag_url = 'http://pickycook.co.kr/recipe/?search=' + self.content
#         return tag_url
#
#
# class RecipeTag(models.Model):
#     recipe = models.ForeignKey(Recipe)
#     tag = models.ForeignKey(Tag)
#     created = models.DateTimeField(auto_now_add=True)
