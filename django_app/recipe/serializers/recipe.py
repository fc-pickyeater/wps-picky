from rest_framework import serializers

from recipe.models import Recipe, Tag
from ..serializers import RecipeStepListSerializer, RecipeReviewListSerializer

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
    reviews = RecipeReviewListSerializer(many=True, required=False, )

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
            'tag',
            'rate_sum',
            'cal_sum',
            'like_count',

            'reviews',
            'recipes',
        )

        # user는 수정되서는 안되기때문에 read_only_fields에 정의
        read_only_fields = (
            'user',
            'rate_sum',
            'cal_sum',
            'like_count',

        )

    # 반환되는 'tag'의 값을 override하기 위한 함수 (tag id가 기존값)
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        tag_contents = []
        # 기존 tag 값(tag id)을 순회하며
        for tag_id in ret['tag']:
            # Tag 테이블에서 값을 찾아
            tag_content = Tag.objects.get(pk=tag_id)
            # tag_contents 리스트에 추가
            tag_contents.append('#' + tag_content.content)
        # 순회가 끝나면 ', '로 조인하여 합침
        tag_list = ', '.join(tag_contents)
        # 'tag' 키로 반환
        ret['tag'] = tag_list
        return ret


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
            'tag',
        )
        read_only_fields = (
            'created_date',
        )

    # 반환되는 'tag'의 값을 override하기 위한 함수 (tag id가 기존값)
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        tag_contents = []
        # 기존 tag 값(tag id)을 순회하며
        for tag_id in ret['tag']:
            # Tag 테이블에서 값을 찾아
            tag_content = Tag.objects.get(pk=tag_id)
            # tag_contents 리스트에 추가, 각 태그앞에 '#' 추가
            tag_contents.append('#' + tag_content.content)
        # 순회가 끝나면 ', '로 조인하여 합침
        tag_list = ', '.join(tag_contents)
        # 'tag' 키 값에 override
        ret['tag'] = tag_list

        # 반환값에 user 추가
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
