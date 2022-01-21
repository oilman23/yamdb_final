from django.contrib.auth import get_user_model
from rest_framework import permissions

from users.models import UserRole

User = get_user_model()


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == UserRole.USER and obj.author == request.user
        )


class IsAuthorOrReadOnlyOrAdminOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        return (
            request.user.role in [UserRole.ADMIN, UserRole.MODERATOR]
            or obj.author == request.user
        )


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
        )
