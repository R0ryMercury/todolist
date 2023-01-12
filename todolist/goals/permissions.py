from rest_framework import permissions


class GoalCategoryPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "user"):
            return (
                request.user
                and request.user.is_authenticated
                and obj.user == request.user
            )
        return (
            request.user and request.user.is_authenticated and obj.user == request.user
        )


class GoalPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "user"):
            return (
                request.user
                and request.user.is_authenticated
                and obj.user == request.user
            )
        return (
            request.user and request.user.is_authenticated and obj.user == request.user
        )


class CommentPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
