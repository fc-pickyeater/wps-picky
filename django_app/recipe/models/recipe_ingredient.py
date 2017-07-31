from django.db import models

from ingredient.models import Ingredient
from recipe.models import RecipeTitle


class Recipe_Ingredient(models.Model):
    # 레시피
    recipe = models.ForeignKey(RecipeTitle)
    # 재료
    ingredient = models.ForeignKey(Ingredient)
    # 구분
    type = models.CharField(max_length=30)
    # 갯수
    amount = models.CharField(max_length=30)
    # 재료이름
    ingre_name = models.CharField(max_length=30)
