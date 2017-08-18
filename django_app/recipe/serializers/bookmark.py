from rest_framework import serializers

from member.models import PickyUser
from recipe.models import BookMark
from recipe.models import Recipe


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

