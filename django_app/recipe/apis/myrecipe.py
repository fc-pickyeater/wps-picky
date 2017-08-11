# 마이페이지에서 자신이 작성한 Recipe 목록 확인
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer
from recipe.serializers.bookmark import BookMarkSerializer
from utils.permissions import ObjectIsRequestUser

__all__ = (
    'MyRecipeListView',
    'BookMarkView',
)


class MyRecipeListView(generics.ListAPIView):
    # RecipeSerializer 사용
    serializer_class = RecipeSerializer
    # IsAuthenticated 클래스와 커스텀 퍼미션 ObjectIsRequestUser 사용
    permission_classes = (
        permissions.IsAuthenticated, ObjectIsRequestUser,
    )

    def get_queryset(self):
        user = self.request.user
        return user.recipe_set.filter(user_id=user)
        # return user.recipe_set.all()


class BookMarkView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, **kwargs):
        user_ = request.user
        recipe_ = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        serializer = BookMarkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user_, recipe=recipe_)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
