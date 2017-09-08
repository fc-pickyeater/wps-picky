from rest_framework import serializers

from recipe.models import BookMark, Recipe
from recipe.serializers.recipe import RecipeListSerializer


class BookMarkSerializer(serializers.ModelSerializer):
    # img_recipe = RecipeListSerializer(many=True)
    # img_recipe = serializers.ImageField(allow_null=True, required=False)
    # img_recipe = serializers.ImageField(default=Recipe.img_recipe)

    class Meta:
        model = BookMark
        fields = (
            'pk',
            'user',
            'recipe',
            # 'img_recipe',
            'memo',
            'created_date',

        )

        read_only_fields = (
            'user',
            'recipe',
            # 'img_recipe',
            'created_date'
        )

    memo = serializers.CharField(required=False)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        recipe = Recipe.objects.get(pk=instance.recipe.pk)
        ret['title'] = recipe.title
        ret['ingredient'] = recipe.ingredient
        ret['rate_sum'] = recipe.rate_sum
        ret['like_count'] = recipe.like_count
        # img_recipe의 값이 없을 경우 에러 발생함. 9/6 Joe
        domain = 'https://s3.ap-northeast-2.amazonaws.com/picky-bucket/'
        if recipe.img_recipe.name:
            ret['img_recipe'] = domain + recipe.img_recipe.name
        else:
            ret['img_recipe'] = None
        # try:
        #     img_path = recipe.img_recipe
        # except ValueError:
        #     ret['img_recipe'] = None
        # else:
        #     ret['img_recipe'] = img_path
        return ret
