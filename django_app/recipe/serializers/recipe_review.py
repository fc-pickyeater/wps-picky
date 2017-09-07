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

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['nickname'] = instance.user.nickname
        return ret


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
            raise CustomValidationError({"content_error": "후기 내용을 채워주세요."})
        else:
            return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['nickname'] = instance.user.nickname
        return ret


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

    content = serializers.CharField(required=False)

    def validate(self, data):
        content = self.initial_data.get('content', '')
        if content == '':
            raise CustomValidationError({"content_error": "후기 내용을 채워주세요."})
        else:
            return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['nickname'] = instance.user.nickname
        return ret
