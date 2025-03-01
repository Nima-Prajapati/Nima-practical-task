from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework import permissions


class SimplePermission(BasePermission):
    """
    Simple permission to prevent code duplication in has_permission & has_object_permission
    """

    def has_access(self, request, view, instance=None):
        raise NotImplementedError

    def has_permission(self, request, view):
        return self.has_access(request, view)

    def has_object_permission(self, request, view, obj):
        return self.has_access(request, view, instance=obj)

    class Meta:
        abstract = True


class IsReadAction(SimplePermission):
    def has_access(self, request, view, instance=None):
        return request.method in SAFE_METHODS


IsEditAction = ~IsReadAction


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                obj == request.user
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only admins to create, update, and delete categories.
    Everyone can read (GET requests).
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # Allow GET requests for everyone
        return request.user and request.user.is_staff