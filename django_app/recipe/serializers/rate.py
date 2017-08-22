from rest_framework import serializers

from recipe.models.recipe import RecipeRate
from utils.exceptions import CustomValidationError


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
        rate = self.initial_data.get('rate', '')
        if rate == '':
            raise CustomValidationError({"rate_error": "값을 입력해주세요."})
        if data['rate'] < 0:
            raise CustomValidationError({"rate_less_error": "평점의 범위를 벗어났습니다."})
        elif data['rate'] > 10:
            raise CustomValidationError({"rate_greater_error": "평점의 범위를 벗어났습니다."})
        else:
            return data
