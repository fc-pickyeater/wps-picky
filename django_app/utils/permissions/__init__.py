from rest_framework import permissions

from recipe.models import RecipeStep


# 8/1 hong 추가 유저 인증관련 instagram에서 가져옴 - hong 8/1
class ObjectIsRequestUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


# ObjectsIsRequestRecipe에서 ObjectIsRequestRecipeStep로 수정

class ObjectIsRequestRecipeStep(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if RecipeStep.objects.filter(recipe=obj.recipe_id):
            if obj.recipe.user == request.user:
                return True

