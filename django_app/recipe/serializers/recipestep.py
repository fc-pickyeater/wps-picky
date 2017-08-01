from rest_framework import serializers

from recipe.models import RecipeStep
from recipe.models import recipestep


class RecipeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeStep
        fields = (
            'recipe_id',
            'step',
            'description',
            'is_timer',
            'timer',
            'image_step',
        )
