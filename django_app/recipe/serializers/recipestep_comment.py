from rest_framework import serializers

from recipe.models.recipe import RecipeStepComment

__all__ = (
    'RecipeStepCommentListSerializer',
    'RecipeStepCommentCreateSerializer',
    'RecipeStepCommentModifySerializer',
)


class RecipeStepCommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStepComment

        fields = (
            'pk',
            'recipe_step',
            'user',
            'content',
        )
        read_only_fields = (
            'recipe_step',
            'user',
        )


class RecipeStepCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStepComment

        fields = (
            'pk',
            'user',
            'recipe_step',
            'content',
            'created_date',
        )

        read_only_fields = (
            'user',
            'recipe_step',
            'created_date',
        )


class RecipeStepCommentModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStepComment

        fields = (
            'user',
            'recipe_step',
            'content',
            'created_date',  # model에 modify_date 만들어서 교체해야할듯? - 8/7 hong
        )
        read_only_fields = (
            'created_date',
            'user',
            'recipe_step',
        )