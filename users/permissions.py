from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Проверка на суперпользователя."""

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsExecutor(BasePermission):
    """Проверка является ли пользователь исполнителем задачи."""

    def has_object_permission(self, request, view, obj):
        executors = [executor for executor in obj.executor.all()]
        return request.user in executors
