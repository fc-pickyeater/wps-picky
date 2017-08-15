from rest_framework import serializers

from recipe.models import Recipe
from recipe.serializers.recipestep import RecipeStepListSerializer

__all__ = (
    'RecipeSerializer',
    'RecipeListSerializer',
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
            'user',
            'img_recipe',
            'description',
            'ingredient',
            'rate_sum',
            'cal_sum',
            'like_count',

            'recipes',
        )
        # user는 수정되서는 안되기때문에 read_only_fields에 정의
        read_only_fields = (
            'user',
            'rate_sum',
            'cal_sum',
            'like_count',
        )


# Recipe 리스트 조회에 사용되는 Serializer
class RecipeListSerializer(serializers.ModelSerializer):

    class Meta:
        # Recipe 모델 사용
        model = Recipe
        fields = (
            'pk',
            'title',
            'user',
            'img_recipe',
            'description',
            'rate_sum',
            'cal_sum',
        )


class RecipeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        # Recipe 모델 사용
        model = Recipe
        fields = (
            'pk',
            'title',
            'description',
            'created_date',
        )

        read_only_fields = (
            'created_date',
        )


    # API 리턴에 키, 값을 추가해주는 함수
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user = instance.user
        ret['user'] = user.pk
        return ret



class RecipeSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'pk',
            'title',
            'user',
            'img_recipe',
            'description',
        )

        # read_only_fields = (
        #     'pk',
        #     'title',
        #     'user',
        #     'img_recipe',
        #     'description',
        #
        # )
