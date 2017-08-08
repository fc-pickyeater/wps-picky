from rest_framework import serializers

from recipe.models import Recipe
from recipe.serializers.recipestep import RecipeStepListSerializer

__all__ = (
    'RecipeSerializer',
)


# Recipe 조회, 수정, 삭제에 사용되는 Serializer
class RecipeSerializer(serializers.ModelSerializer):
    # Recipe안에 RecipeStep들을 보여주기위해
    # RecipeStepListSerializer 사용
    # 여러 객체들을 가져오기위해 many=True옵션 설정(필수)
    recipes = RecipeStepListSerializer(many=True)

    class Meta:
        # Recipe 모델 사용
        model = Recipe
        fields = (
            'pk',
            'title',
            'img_recipe',
            'description',
            'recipes',
        )
        # user는 수정되서는 안되기때문에 read_only_fields에 정의
        read_only_fields = (
            'user',
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'pk',
            'title',
            'description',
        )
