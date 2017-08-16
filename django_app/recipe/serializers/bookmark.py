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


class BookMarkUpdateSeriailizer(serializers.ModelSerializer):
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

    def validate_user(self, user):
        if user in PickyUser.bookmark_set.filter(user=user).exists():
            raise serializers.ValidationError("이미 사용중 입니다.")
        return user

    def validated_recipe(self, recipe):
        if recipe in Recipe.objects.filter(recipe=recipe).exists():
            raise serializers.ValidationError("이미 사용중 입니다.")
        return recipe
