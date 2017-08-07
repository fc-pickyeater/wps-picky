from rest_framework import serializers

from recipe.models import Recipe
from recipe.serializers import RecipeStepListSerializer


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
