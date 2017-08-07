from rest_framework import generics
from rest_framework import permissions

from member.models import PickyUser
from recipe.models import RecipeStep
from recipe.serializers import RecipeCreateSerializer
from recipe.serializers import RecipeModifySerializer
from utils.permissions import ObjectIsRequestUser, ObjectIsRequestRecipe


# recipecreateview 생성 - hong 8/1
class RecipestepCreateView(generics.CreateAPIView):
    queryset = RecipeStep.objects.all()
    permission_classes = (permissions.IsAuthenticated, ObjectIsRequestUser,)
    serializer_class = RecipeCreateSerializer


# recipemodifyview 생성 - hong 8/2
class RecipestepModifyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeStep.objects.all()
    permission_classes = (permissions.IsAuthenticated, ObjectIsRequestRecipe,)
    serializer_class = RecipeModifySerializer

