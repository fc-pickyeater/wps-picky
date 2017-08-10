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
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=RecipeStep.objects.all(),
                fields=('recipe', 'step'),
                message=("레시피에 이미 스탭이 존재합니다.")
            )
        ]


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
    def __init__(self, *args, **kwargs):
        super(RecipeModifySerializer, self).__init__(*args, **kwargs)

        self.fields['description'].error_messages['blank'] = u'빈값을 넣으면 안됩니다.'

    class Meta:
        model = RecipeStep

        fields = (
            'pk',
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

# cass RecipeStepDeleteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RecipeStep
