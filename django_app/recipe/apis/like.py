# 마이페이지에서 자신이 작성한 Recipe 목록 확인
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.models import Recipe
from recipe.models.recipe import RecipeLike
from recipe.serializers.recipelike import RecipeLikeSerializer


# 레시피 좋아요 view
class RecipeLikeView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, **kwargs):

        user_ = request.user
        # recipe_ = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        try:
            recipe_ = Recipe.objects.get(pk=kwargs.get('recipe_pk'))
        except AttributeError:
            return Response(
                {
                    "detail": "레시피를 찾을 수 없습니다.",
                    "status_code": status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RecipeLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 레시피에 이미 좋아요를 눌렀는지 판단
        if RecipeLike.objects.filter(user=user_, recipe=recipe_).exists():
            return Response(
                {
                    "detail": "이미 좋아요를 눌렀습니다.",
                    "status_code": status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            # 좋아요 생성
            serializer.save(user=user_, recipe=recipe_)
            # 좋아요 생성과 동시에 좋아요 개수 카운트
            recipe_.like_count = recipe_.recipelike_set.count()
            recipe_.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        # delete 요청시

    def delete(self, request, **kwargs):
        # 레시피를 가져온다
        # recipe_instance = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        try:
            recipe_instance = Recipe.objects.get(pk=kwargs.get('recipe_pk'))
        except:
            return Response(
                {
                    "detail": "레시피를 찾을 수 없습니다.",
                    "status_code": status.HTTP_404_NOT_FOUND},

                status=status.HTTP_404_NOT_FOUND
            )
        instance = get_object_or_404(recipe_instance.recipelike_set, user=request.user)
        # 삭제
        instance.delete()
        # 삭제와 동시에 좋아요 개수 카운트
        recipe_instance.like_count = recipe_instance.recipelike_set.count()
        recipe_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
