from rest_framework import generics

from recipe.models import RecipeStep
from recipe.serializers import RecipeCreateSerializer


class RecipeCreateView(generics.CreateAPIView):
    serializer_class = RecipeCreateSerializer

