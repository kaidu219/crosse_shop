from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Пользователь может изменять и удалять свою информацию,
    администратор может изменять и удалять любую информацию.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff
