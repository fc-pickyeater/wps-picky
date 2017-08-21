from rest_framework import serializers

from recipe.models import Recipe
from recipe.models import Tag


class RecipeSearchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'pk',
            'title',
            'user',
            'description',
            'img_recipe',
            'ingredient',
            'cal_sum',
            'tag',
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
