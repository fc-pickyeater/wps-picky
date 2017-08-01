from rest_framework import serializers

from ingredient.models import Ingredient

__all__ = (
    'IngredientSerializer',
    'IngredientUpdateSerializer',
)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'pk',
            'name',
            'description',
            'unit',
            'cal',

        )


class IngredientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'name',
            'description',
            'unit',
            'cal',
        )
