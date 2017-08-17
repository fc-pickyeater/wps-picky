from rest_framework import serializers

from utils.exceptions import CustomValidationError
from ..models.recipe import RecipeReview

__all__ = (
    'RecipeReviewCreateSerializer',
    'RecipeReviewModifySerializer',
    'RecipeReviewListSerializer',
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
        )

        read_only_fields = (
            'recipe',
            'user',
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
            'created_date',
        )

    content = serializers.CharField(required=False)

    def validate(self, data):
        content = self.initial_data.get('content', '')
        if content == '':
            raise CustomValidationError({"content": "후기 내용을 채워주세요."})
        else:
            return data


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
