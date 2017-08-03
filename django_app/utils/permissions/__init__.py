from rest_framework import permissions


# 8/1 hong 추가 유저 인증관련 instagram에서 가져옴 - hong 8/1
class ObjectIsRequestUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            print(obj.user)
            return True
        return obj.user == request.user




