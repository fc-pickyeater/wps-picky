from rest_framework import permissions

from recipe.models import RecipeStep

__all__ = (
    'ObjectIsRequestRecipeStep',
    'ObjectIsRequestUser',
)


# 8/1 hong 추가 유저 인증관련 instagram에서 가져옴 - hong 8/1
class ObjectIsRequestUser(permissions.BasePermission):
    message = '유저가 다릅니다'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


# ObjectsIsRequestRecipe에서 ObjectIsRequestRecipeStep로 수정

class ObjectIsRequestRecipeStep(permissions.BasePermission):
    message = '유저가 다릅니다'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if RecipeStep.objects.filter(recipe=obj.recipe_id).exists():
            if obj.recipe.user == request.user:
                return True

