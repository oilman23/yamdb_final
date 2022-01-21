from django.contrib.auth import get_user_model
from rest_framework import permissions
from users.models import UserRole

User = get_user_model()


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRole.ADMIN
