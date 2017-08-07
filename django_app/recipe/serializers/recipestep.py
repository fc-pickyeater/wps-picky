from rest_framework import serializers

from recipe.models import RecipeStep

__all__ = (
    'RecipeCreateSerializer',
    'RecipeStepListSerializer',
    'RecipeModifySerializer',
    # 'RecipeStepDeleteSerializer',
)

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


class RecipeStepListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = (
            'pk',
            'step',
            'description',
            'is_timer',
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

# class RecipeStepDeleteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RecipeStep