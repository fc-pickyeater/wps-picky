from rest_framework import serializers

from recipe.models import RecipeStep


# recipestepserializer 생성 - hong 8/1
class RecipeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = (
            'recipe',
            'step',
            'description',
            'is_timer',
            'timer',
            'image_step',
        )


# recipestepmodifyserializer 생성 - hong 8/2
class RecipeModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = (
            'description',
            'is_timer',
            'timer',
            'image_step',
        )
        read_only_fields = (
            'recipe',
            'step',
        )
