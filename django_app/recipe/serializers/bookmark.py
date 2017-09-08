from rest_framework import serializers

from recipe.models import BookMark, Recipe


class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        fields = (
            'pk',
            'user',
            'recipe',
            'memo',
            'created_date',

        )

        read_only_fields = (
            'user',
            'recipe',
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
        ret['img_recipe'] = recipe.img_recipe.path
        # try:
        #     img_path = recipe.img_recipe.path
        # except ValueError:
        #     ret['img_recipe'] = None
        # else:
        #     ret['img_recipe'] = img_path
        return ret
