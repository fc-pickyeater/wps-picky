from rest_framework import generics
from rest_framework import permissions

from recipe.models import RecipeStep
from recipe.models import RecipeStepComment
from recipe.serializers import RecipeStepCommentListSerializer
from recipe.serializers.recipestep_comment import RecipeStepCommentCreateSerializer, RecipeStepCommentModifySerializer
from utils.permissions import ObjectIsRequestUser

__all__ = (
    'RecipeStepCommentListView',
    'RecipeStepCommentCreateView',
    'RecipeStepCommentModifyView',
)


# 레시피 스탭에 달려있는 코멘트 리스트를 보여주는 API - 8/7 hong
class RecipeStepCommentListView(generics.ListAPIView):
    queryset = RecipeStepComment.objects.all()
    serializer_class = RecipeStepCommentListSerializer


# 레시피 스텝에 코멘트를 작성하는 API -8/7 hong
class RecipeStepCommentCreateView(generics.CreateAPIView):
    """
    method: POST
    pk: 레시피스탭의 pk
    """
    # 로그인한 유저라면 모두 댓글작성이 가능함
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = RecipeStepCommentCreateSerializer
    queryset = RecipeStepComment.objects.all()

    # 생성하는 함수
    # step_pk 레시피 스탭의 pk
    def perform_create(self, serializer):
        step_pk = self.kwargs['pk']
        serializer.save(
            user=self.request.user,
            recipe_step=RecipeStep.objects.get(pk=step_pk),
        )


# 레시피 스탭 코멘트를 수정,삭제하는 API - 8/7
class RecipeStepCommentModifyView(generics.RetrieveUpdateDestroyAPIView):
    """
    method: PATCH 수정
            DELETE 삭제
    """
    permission_classes = (
        permissions.IsAuthenticated, ObjectIsRequestUser,
    )

    def get_queryset(self):
        comment = RecipeStepComment.objects.filter(user=self.request.user)
        return comment

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return RecipeStepCommentModifySerializer