from rest_framework import generics

from recipe.models import RecipeStep
from recipe.serializers import RecipeCreateSerializer

# recipecreateview 생성 - hong 8/1
class RecipeCreateView(generics.CreateAPIView):
    serializer_class = RecipeCreateSerializer

