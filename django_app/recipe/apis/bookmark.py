from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.models import BookMark
from recipe.models import Recipe
from recipe.serializers.bookmark import BookMarkSerializer
from utils.permissions import ObjectIsRequestUser

__all__ = (
    'BookMarkListView',
    'BookMarkView',
)


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
        try:
            recipe_ = Recipe.objects.get(pk=kwargs.get('recipe_pk'))
        except:
            return Response(
                {
                    "detail": "레시피를 찾을 수 없습니다.",
                    "status_code": status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = BookMarkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if BookMark.objects.filter(user=user_, recipe=recipe_).exists():
            return Response(
                {
                    "detail": "이미 북마크 되었습니다.",
                    "status_code": status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )
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
        # recipe_ = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        try:
            recipe_ = Recipe.objects.get(pk=kwargs.get('recipe_pk'))
        except:
            return Response(
                {
                    "detail": "레시피를 찾을 수 없습니다.",
                    "status_code": status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )
        instance = get_object_or_404(BookMark, user=user_, recipe=recipe_)
        serializer = BookMarkSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete 요청시
    def delete(self, request, **kwargs):
        # 북마크를 가져온다
        # recipe_instance = get_object_or_404(Recipe, pk=kwargs.get('recipe_pk'))
        try:
            recipe_instance = Recipe.objects.get(pk=kwargs.get('recipe_pk'))
        except:
            return Response(
                {
                    "detail": "레시피를 찾을 수 없습니다.",
                    "status_code": status.HTTP_404_NOT_FOUND
                },
                status=status.HTTP_404_NOT_FOUND
            )
        instance = get_object_or_404(recipe_instance.bookmark_set, user=request.user)
        instance.delete()
        recipe_instance.bookmark_count = recipe_instance.bookmark_set.count()
        recipe_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
