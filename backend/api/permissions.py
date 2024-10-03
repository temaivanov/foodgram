from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Запрещает пользователям изменять данные профилей друг друга."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj == request.user
        )


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    """Доступ для автора и суперюзера."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user == obj.author
                or request.user.is_superuser
                )
