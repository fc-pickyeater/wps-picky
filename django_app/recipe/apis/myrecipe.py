# 마이페이지에서 자신이 작성한 Recipe 목록 확인
from rest_framework import generics
from rest_framework import permissions

from recipe.serializers import RecipeListSerializer
from utils.permissions import ObjectIsRequestUser

__all__ = (
    'MyRecipeListView',

)


class MyRecipeListView(generics.ListAPIView):
    # RecipeSerializer 사용
    serializer_class = RecipeListSerializer
    # IsAuthenticated 클래스와 커스텀 퍼미션 ObjectIsRequestUser 사용
    permission_classes = (
        permissions.IsAuthenticated, ObjectIsRequestUser,
    )

    def get_queryset(self):
        user = self.request.user
        return user.recipe_set.filter(user_id=user)
        # return user.recipe_set.all()


