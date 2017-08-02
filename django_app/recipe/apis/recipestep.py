from rest_framework import generics
from rest_framework import permissions

from recipe.serializers import RecipeCreateSerializer
from utils.permissions import ObjectIsRequestUser

# recipecreateview 생성 - hong 8/1



class RecipeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, ObjectIsRequestUser,)
    serializer_class = RecipeCreateSerializer
