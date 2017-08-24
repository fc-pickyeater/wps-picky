# 마이페이지에서 자신이 작성한 Recipe 목록 확인
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.models import Recipe
from recipe.models.recipe import RecipeRate
from recipe.serializers import RecipeRateSerializer


# 평점 주는 view
class RecipeRateView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, **kwargs):
        user_ = request.user
        # recipe_ = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        try:
            recipe_ = Recipe.objects.get(pk=kwargs.get('recipe_pk'))
        except:
            return Response(
                {
                    "recipe_not_found": "레시피를 찾을 수 없습니다.",
                    "status_code": status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = RecipeRateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 평점을 주었는지 판단
        if RecipeRate.objects.filter(user=user_, recipe=recipe_).exists():
            return Response(
                {
                    "already_rated": "이미 평점을 주었습니다.",
                    "status_code": status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            # 평점을 저장
            serializer.save(user=user_, recipe=recipe_)
            # 저장후 평점 개수 카운트
            cnt = RecipeRate.objects.filter(recipe=recipe_).count()
            # 현재 레시피의 평점을 가져옴
            avg = recipe_.rate_sum
            # 유저가 주는 평점
            current_rate = float(serializer.data.get('rate'))
            # 다시 평점을 계산하는 공식
            new_avg = float((avg * (cnt - 1) + current_rate) / cnt)
            # 대입 후 저장
            recipe_.rate_sum = new_avg
            recipe_.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, **kwargs):
        # 접속한 유저
        user_ = request.user
        # pk로 받은 recipe
        # recipe_ = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        try:
            recipe_ = Recipe.objects.get(pk=kwargs.get('recipe_pk'))
        except:
            return Response(
                {
                    "recipe_not_found": "레시피를 찾을 수 없습니다.",
                    "status_code": status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )
        instance = get_object_or_404(RecipeRate, user=user_, recipe=recipe_)
        serializer = RecipeRateSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 공식에 관한설명은 post부분 참조
        cnt = RecipeRate.objects.filter(recipe=recipe_).count()
        avg = recipe_.rate_sum
        current_rate = float(serializer.data.get('rate'))
        new_avg = float((avg * (cnt - 1) + current_rate) / cnt)
        recipe_.rate_sum = new_avg
        recipe_.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        # 레시피를 가져온다
        # recipe_instance = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        try:
            recipe_instance = Recipe.objects.get(pk=kwargs.get('recipe_pk'))
        except:
            return Response(
                {
                    "recipe_not_found": "레시피를 찾을 수 없습니다.",
                    "status_code": status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )
        instance = get_object_or_404(recipe_instance.reciperate_set, user=request.user)
        # 공식 관련 부분은 post참조
        cnt = RecipeRate.objects.filter(recipe=recipe_instance).count()
        avg = recipe_instance.rate_sum
        current_rate = float(RecipeRate.objects.get(user=request.user).rate)
        # 평점이 하나만 있을때 나누기 오류가 남
        # 그부분을 잡기위한 try-except문
        try:
            new_avg = float(((avg * cnt) - current_rate) / (cnt - 1))
        except:
            new_avg = 0
        recipe_instance.rate_sum = new_avg
        recipe_instance.save()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
