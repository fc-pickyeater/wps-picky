# 마이페이지에서 자신이 작성한 Recipe 목록 확인
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.models import BookMark
from recipe.models import Recipe
from recipe.serializers import RecipeSerializer
from recipe.serializers.bookmark import BookMarkSerializer
from recipe.serializers.recipelike import RecipeLikeSerializer
from utils.permissions import ObjectIsRequestUser

__all__ = (
    'MyRecipeListView',
    'BookMarkListView',
    'BookMarkView',
    'RecipeLikeView',

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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # patch 요청시
    def patch(self, request, **kwargs):
        # 접속한 유저
        user_ = request.user
        # pk로 받은 recipe
        recipe_ = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        instace = get_object_or_404(BookMark,user=user_,recipe=recipe_)
        serializer = BookMarkSerializer(instace, data=request.data )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete 요청시
    def delete(self, request, **kwargs):
        # 북마크를 가져온다
        recipe_instance = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        instance = get_object_or_404(recipe_instance.bookmark_set, user=request.user)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeLikeView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, **kwargs):

        user_ = request.user
        recipe_ = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        serializer = RecipeLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if BookMark.objects.filter(user=user_, recipe=recipe_).exists():
            return Response({"detail": "이미 좋아요를 눌렀습니다."}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer.save(user=user_, recipe=recipe_)
            recipe_.like_count = recipe_.recipelike_set.count()
            recipe_.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        # delete 요청시

    def delete(self, request, **kwargs):
        # 레시피를 가져온다
        recipe_instance = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        instance = get_object_or_404(recipe_instance.recipelike_set, user=request.user)
        instance.delete()
        recipe_instance.like_count = recipe_instance.recipelike_set.count()
        recipe_instance.save()
        return Response({"detail": "asdasd"}, status=status.HTTP_204_NO_CONTENT)

# if hasattr(request.data, '_mutable'):
#            request.data._mutable = True
#        request.data['user'] = user_.pk
#        request.data['recipe'] = recipe_.pk
