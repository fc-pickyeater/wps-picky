from django.db import models

from ingredient.models import Ingredient
from ..models import Recipe

__all__ = (
    'RecipeIngredient',
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
