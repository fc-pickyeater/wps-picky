from rest_framework import serializers

from recipe.models import Recipe
from recipe.serializers.recipestep import RecipeStepListSerializer

__all__ = (
    'RecipeSerializer',
)


class RecipeSerializer(serializers.ModelSerializer):
    recipes = RecipeStepListSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'pk',
            'title',
            'img_recipe',
            'description',
            'recipes',
        )
        read_only_fields = (
            'user',
        )
