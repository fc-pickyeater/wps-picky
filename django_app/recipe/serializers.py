from django.forms import widgets
from rest_framework import serializers
from .models import Recipe

# 8/1 승팔씀
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'pk',
            'title',
            'img_recipe',
        )



