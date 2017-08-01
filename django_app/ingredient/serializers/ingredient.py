from rest_framework import serializers

from ingredient.models import Ingredient

__all__ = (
    'IngredientSerializer',
    # 'IngredientUpdateSerializer',
)

# ingredientserializer 생성 - hong 8/1
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'pk',
            'name',
            'description',
            'unit',
            'cal',

        )

# 8/1 기준 사용하지 않는 serializer
# class IngredientUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ingredient
#         fields = (
#             'name',
#             'description',
#             'unit',
#             'cal',
#         )
