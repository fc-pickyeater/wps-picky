from rest_framework import serializers

from recipe.models import Tag


__all__ = (
    'RecipeTagCreateSerializer',
)


# 이방법이 아닌거같음... 8/14 joe
class RecipeTagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'content',
            'url',
        )
