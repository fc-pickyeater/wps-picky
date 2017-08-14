from rest_framework import serializers

from recipe.models.recipe import RecipeLike


class RecipeLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeLike

        fields = (
            'pk',
            'user',
            'recipe',
        )

        read_only_fields = (
            'user',
            'recipe',
            'created_date',
        )
