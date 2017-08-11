from rest_framework import serializers

from recipe.models.recipe import RecipeStep
from recipe.serializers.recipestep_comment import RecipeStepCommentListSerializer

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
            'pk',
            'recipe',
            'step',
            'description',
            'is_timer',
            'timer',
            'image_step',
        )
        # 위에서 가져온 step 필드를 override하여 키, 값이 없어도 통과하게함 8/10 joe
        step = serializers.IntegerField(required=False, allow_null=True)


class RecipeStepListSerializer(serializers.ModelSerializer):
    comments = RecipeStepCommentListSerializer(many=True)

    class Meta:
        model = RecipeStep
        fields = (
            'pk',
            'step',
            'description',
            'is_timer',
            'timer',
            'image_step',
            'comments',
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


