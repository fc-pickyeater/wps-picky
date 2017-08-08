from rest_framework import generics
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from recipe.models import RecipeStep
from recipe.models import RecipeStepComment
from recipe.serializers import RecipeStepCommentListSerializer
from recipe.serializers.recipestep_comment import RecipeStepCommentCreateSerializer

__all__ = (
    'RecipeStep_CommentListView',
    'RecipeStep_CommentCreateView',
)


class RecipeStep_CommentListView(generics.ListAPIView):
    queryset = RecipeStepComment.objects.all()
    serializer_class = RecipeStepCommentListSerializer


class RecipeStep_CommentCreateView(generics.CreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = RecipeStepCommentCreateSerializer

    def perform_create(self, serializer):
        recipe_step = get_object_or_404(RecipeStep, pk=self.request.data.get('recipe_step'))
        serializer.save(author=self.request.user, recipe_step=recipe_step)