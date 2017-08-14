from rest_framework import serializers

from recipe.models.recipe import RecipeRate


class RecipeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeRate

        fields = (
            'pk',
            'user',
            'recipe',
            'rate',
        )

        read_only_fields = (
            'user',
            'recipe',
        )
