# 마이페이지에서 자신이 작성한 Recipe 목록 확인
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.models import BookMark
from recipe.models import Recipe
from recipe.models.recipe import RecipeLike, RecipeRate
from recipe.serializers import RecipeRateSerializer
from recipe.serializers import RecipeSerializer
from recipe.serializers.bookmark import BookMarkSerializer
from recipe.serializers.recipelike import RecipeLikeSerializer
from utils.permissions import ObjectIsRequestUser

__all__ = (
    'MyRecipeListView',
    'BookMarkListView',
    'BookMarkView',
    'RecipeLikeView',
    'RecipeRateView',

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


# 북마크한 레시피를 보여주는 리스트
class BookMarkListView(APIView):
    permission_classes = (
        permissions.IsAuthenticated, ObjectIsRequestUser
    )

    def get(self, request, format=None):
        bookmarklist = BookMark.objects.filter(user=request.user)
        serializer = BookMarkSerializer(bookmarklist, many=True)
        return Response(serializer.data)


# 북마크 하는 API
class BookMarkView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    # post 요청시
    def post(self, request, **kwargs):
        # 접속한 유저
        user_ = request.user

        # pk로 받은 recipe
        recipe_ = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        serializer = BookMarkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if BookMark.objects.filter(user=user_, recipe=recipe_).exists():
            return Response({"detail": "이미 북마크 되었습니다."}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer.save(user=user_, recipe=recipe_)
            recipe_.bookmark_count = recipe_.bookmark_set.count()
            recipe_.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # patch 요청시
    def patch(self, request, **kwargs):
        # 접속한 유저
        user_ = request.user
        # pk로 받은 recipe
        recipe_ = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        instance = get_object_or_404(BookMark, user=user_, recipe=recipe_)
        serializer = BookMarkSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete 요청시
    def delete(self, request, **kwargs):
        # 북마크를 가져온다
        recipe_instance = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        instance = get_object_or_404(recipe_instance.bookmark_set, user=request.user)
        instance.delete()
        recipe_instance.bookmark_count = recipe_instance.bookmark_set.count()
        recipe_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 레시피 좋아요 view
class RecipeLikeView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, **kwargs):

        user_ = request.user
        recipe_ = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        serializer = RecipeLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 레시피에 이미 좋아요를 눌렀는지 판단
        if RecipeLike.objects.filter(user=user_, recipe=recipe_).exists():
            return Response({"detail": "이미 좋아요를 눌렀습니다."}, status=status.HTTP_404_NOT_FOUND)
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
        recipe_instance = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        instance = get_object_or_404(recipe_instance.recipelike_set, user=request.user)
        # 삭제
        instance.delete()
        # 삭제와 동시에 좋아요 개수 카운트
        recipe_instance.like_count = recipe_instance.recipelike_set.count()
        recipe_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# if hasattr(request.data, '_mutable'):
#            request.data._mutable = True
#        request.data['user'] = user_.pk
#        request.data['recipe'] = recipe_.pk

# 평점 주는 view
class RecipeRateView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, **kwargs):
        user_ = request.user
        recipe_ = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        serializer = RecipeRateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 평점을 주었는지 판단
        if RecipeRate.objects.filter(user=user_, recipe=recipe_).exists():
            return Response({"detail": "이미 평점을 주었습니다."}, status=status.HTTP_404_NOT_FOUND)
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
        recipe_ = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
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
        recipe_instance = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        instance = get_object_or_404(recipe_instance.reciperate_set, user=request.user)
        # 공식 관련 부분은 post참조
        cnt = RecipeRate.objects.filter(recipe=recipe_instance).count()
        avg = recipe_instance.rate_sum
        current_rate = float(RecipeRate.objects.get(user=request.user).rate)
        new_avg = float(((avg * cnt) - current_rate) / (cnt-1))
        recipe_instance.rate_sum = new_avg
        recipe_instance.save()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
