from rest_framework import serializers
from ..models.recipe import RecipeReview


__all__ = (
    'RecipeReviewCreateSerializer',
    'RecipeReviewModifySerializer',
)


class RecipeReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeReview

        fields = (
            'pk',
            'user',
            'recipe',
            'content',
            'img_review',
            'created_date',
        )

        read_only_fields = (
            'user',
            'recipe',
            'created_date'
        )


class RecipeReviewModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeReview

        fields = (
            'pk',
            'user',
            'recipe',
            'content',
            'img_review',
            'modified_date',
        )

        read_only_fields = (
            'modified_date',
            'user',
            'recipe',
        )