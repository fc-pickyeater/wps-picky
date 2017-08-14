from rest_framework import serializers
from ..models.recipe import RecipeReview


__all__ = (
    'RecipeReviewListSerializer',
    'RecipeReviewCreateSerializer',
    'RecipeReviewModifySerializer',
)


class RecipeReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeReview

        fields = (
            'pk',
            'recipe',
            'user',
            'content',
            'img_review',
            'created_date',
            'modified_date',
        )

        read_only_fields = (
            'recipe',
            'user',
            'created_date',
            'modified_date',
        )


class RecipeReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeReview

        fields = (
            'pk',
            'user',
            'recipe',
            'content',
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
            'modified_date',
        )

        read_only_fields = (
            'modified_date',
            'user',
            'recipe',
        )