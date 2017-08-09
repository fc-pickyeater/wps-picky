from rest_framework import serializers

from ingredient.serializers import IngredientSerializer
from recipe.models.recipe_ingredient import RecipeIngredient
from recipe.serializers import RecipeSerializer
from recipe.serializers.recipe import RecipeSearchSerializer


class RecipeSearchListSerializer(serializers.ModelSerializer):
    recipe = RecipeSearchSerializer()
    # ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = (
            'recipe',
            # 'ingredient',
            'ingre_name',

        )

        read_only_fields = (
            'recipe',
            # 'ingredient',
            'ingre_name',
        )
