from rest_framework import serializers

from recipe.models.recipe import RecipeStep
from recipe.serializers.recipestep_comment import RecipeStepCommentListSerializer
from utils.exceptions import CustomValidationError

__all__ = (
    'RecipeStepCreateSerializer',
    'RecipeStepListSerializer',
    'RecipeModifySerializer',
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
            'img_step',
        )
        # 위에서 가져온 step 필드를 override하여 키, 값이 없어도 통과하게함 8/10 joe
        step = serializers.IntegerField(required=False, allow_null=True)

        read_only_fields = (
            'step',
        )

    description = serializers.CharField(required=False)
    recipe = serializers.CharField(required=False)

    def validate(self, data):
        recipe = self.initial_data.get('recipe', '')
        description = self.initial_data.get('description', '')
        if recipe == '':
            raise CustomValidationError({"recipe": "레시피를 입력하세요."})
        if description == '':
            raise CustomValidationError({"description": "설명을 입력하세요."})
        elif len(data['description']) > 256:
            raise CustomValidationError({"description": "설명이 256자를 초과했습니다."})
        else:
            return data


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
            'img_step',
            'comments',
        )


# recipestepmodifyserializer 생성 - hong 8/2
class RecipeModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep

        fields = (
            'pk',
            'description',
            'is_timer',
            'timer',
            'img_step',
            'recipe',
            'step',
        )

        read_only_fields = (
            'recipe',
            'step',
        )

    description = serializers.CharField(required=False)

    def validate(self, data):
        description = self.initial_data.get('description', '')
        if description == '':
            raise CustomValidationError({"description": "설명을 입력하세요."})
        elif len(data['description']) > 256:
            raise CustomValidationError({"description": "설명이 256자를 초과했습니다."})
        else:
            return data

# cass RecipeStepDeleteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RecipeStep
