from rest_framework import generics
from rest_framework import permissions

from recipe.models import RecipeStep
from recipe.serializers import RecipeCreateSerializer
from recipe.serializers import RecipeModifySerializer
from utils.permissions import ObjectIsRequestUser, ObjectIsRequestRecipeStep


# recipecreateview 생성 - hong 8/1
class RecipeStepCreateView(generics.CreateAPIView):
    queryset = RecipeStep.objects.all()
    permission_classes = (permissions.IsAuthenticated, ObjectIsRequestUser,)
    serializer_class = RecipeCreateSerializer


# recipemodifyview 생성 - hong 8/2
class RecipeStepModifyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeStep.objects.all()
    permission_classes = (permissions.IsAuthenticated, ObjectIsRequestRecipeStep,)
    serializer_class = RecipeModifySerializer


class RecipeStepModifyDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeStep.objects.all()
    permission_classes = (permissions.IsAuthenticated, ObjectIsRequestRecipeStep,)

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return RecipeModifySerializer
