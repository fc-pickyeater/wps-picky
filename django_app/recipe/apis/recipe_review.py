from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from utils.permissions import ObjectIsRequestUser
from ..serializers import RecipeReviewModifySerializer, RecipeReviewCreateSerializer
from ..models import RecipeReview, Recipe


__all__ = (
    'RecipeReviewCreateView',
    'RecipeReviewModifyView',
)

# 레시피에 달리는 후기를 작성하는 API
class RecipeReviewCreateView(generics.CreateAPIView):
    """
    method : POST
    pk : recipe
    """
    # 인증 된 사용자만 생성할 수 있음
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = RecipeReviewCreateSerializer
    queryset = RecipeReview.objects.all()

    # 생성 함수
    def perform_create(self, serializer):
        recipe_pk = self.kwargs['pk']
        serializer.save(
            user=self.request.user,
            recipe=Recipe.objects.get(pk=recipe_pk)
        )


# 레시피 후기 수정, 삭제(삭제 기능은 )
class RecipeReviewModifyView(generics.RetrieveUpdateDestroyAPIView):
    """
    method : PATCH(수정)
            DELETE(삭제)
    """
    # ObjectIsRequestUser(Custom Permission) 사용
    # 수정, 삭제 Request를 보낸 유저가 해당 object의 User인지 인증

    permission_classes = (
        permissions.IsAuthenticated, ObjectIsRequestUser,
    )

    # objects의 user가 request를 보낸 유저와 같은 review 반환
    def get_queryset(self):
        review = RecipeReview.objects.filter(user=self.request.user)
        return review

    # PATCH 메소드의 Request가 오면
    # RecipeReviewModifySerializer 사용
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return RecipeReviewModifySerializer

