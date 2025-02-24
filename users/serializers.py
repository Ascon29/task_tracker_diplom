from rest_framework import serializers

from task_tracker.models import Task
from users.models import User


class ActiveTaskSerializer(serializers.ModelSerializer):
    """Сериализатор списка активных задач.
    Использует метод to_representation для вывода задач только со статусом 'В работе'."""

    class Meta:
        model = Task
        fields = ["id", "name"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.status == "В работе":
            return representation


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор списка сотрудников"""

    active_tasks = ActiveTaskSerializer(source="task_set", many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "job_title", "active_tasks"]


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации сотрудника."""

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "job_title", "password"]
