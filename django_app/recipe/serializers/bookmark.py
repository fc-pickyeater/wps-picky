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
            'created_date',
        )
        unique_together = (
            'user', 'recipe'
        )
