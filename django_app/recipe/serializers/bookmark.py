from rest_framework import serializers

from recipe.models import BookMark


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
        ret['recipe_title'] = instance.recipe.title
        return ret