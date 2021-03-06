from rest_framework import serializers

from recipe.models.recipe import RecipeStepComment
from utils.exceptions import CustomValidationError

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

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['nickname'] = instance.user.nickname
        return ret


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

    content = serializers.CharField(required=False)

    def validate(self, data):
        content = self.initial_data.get('content', '')
        if content == '':
            raise CustomValidationError({"content_error": "댓글의 내용을 적어주세요"})
        if len(data['content']) > 256:
            raise CustomValidationError({"content_length_error": "댓글의 내용이 256자를 초과합니다."})
        else:
            return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['nickname'] = instance.user.nickname
        return ret


class RecipeStepCommentModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStepComment

        fields = (
            'pk',
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

    content = serializers.CharField(required=False)

    def validate(self, data):
        content = self.initial_data.get('content', '')
        if content == '':
            raise CustomValidationError({"content_error": "댓글의 내용을 적어주세요"})
        if len(data['content']) > 256:
            raise CustomValidationError({"content_length_error": "댓글의 내용이 256자를 초과합니다."})
        else:
            return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['nickname'] = instance.user.nickname
        return ret
