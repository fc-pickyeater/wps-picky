from rest_framework import serializers

from recipe.models import RecipeStep

__all__ = (
    'RecipeStepCreateSerializer',
    'RecipeStepListSerializer',
    'RecipeModifySerializer',
    # 'RecipeStepDeleteSerializer',
)


# recipestepserializer 생성 - hong 8/1
class RecipeStepCreateSerializer(serializers.ModelSerializer):
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
            'recipe',
            'step',
        )

        read_only_fields = (
            'recipe',
            'step',
        )

# class RecipeStepDeleteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RecipeStep