from rest_framework import serializers

from recipe.models.recipe import RecipeRate


class RecipeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeRate

        fields = (
            'pk',
            'user',
            'recipe',
            'rate',
        )

        read_only_fields = (
            'user',
            'recipe',
        )

    def validate(self, data):
        if data['rate'] < 0:
            raise serializers.ValidationError('평점의 범위를 벗어났습니다.')
        elif data['rate'] > 10:
            raise serializers.ValidationError('평점의 범위를 벗어났습니다.')
        else:
            return data
