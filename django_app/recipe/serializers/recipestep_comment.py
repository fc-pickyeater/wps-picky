from rest_framework import serializers

from recipe.models.recipe import RecipeStepComment

__all__ = (
    'RecipeStepCommentListSerializer',
    'RecipeStepCommentCreateSerializer',
)


class RecipeStepCommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStepComment

        fields = (
            'recipe_step_id',
            'author_id',
            'content',
        )


class RecipeStepCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStepComment

        fields = (
            'content',
        )

        read_only_fields = (
            'author_id',
            'created_date',
        )
