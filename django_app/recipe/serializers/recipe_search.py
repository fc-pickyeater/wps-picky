from rest_framework import serializers

from recipe.models import Recipe


class RecipeSearchListSerializer(serializers.ModelSerializer):
    # recipe = RecipeSearchSerializer()
    # ingredient = IngredientSerializer()

    class Meta:
        model = Recipe
        fields = (
            'pk',
            'title',
            'user',
            'description',
            'img_recipe',
            'cal_sum',
        )
