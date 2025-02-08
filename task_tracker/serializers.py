from rest_framework import serializers

from task_tracker.models import Task
from task_tracker.validators import TaskValidator


class MaintaskSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода вложенной информации о родительской задаче"""

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "deadline",
            "executor",
        ]


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор для задач."""

    main_task = MaintaskSerializer(source="parent_task", read_only=True)

    class Meta:
        model = Task
        fields = ["id", "name", "description", "is_main_task", "deadline", "status", "executor", "main_task"]
        validators = [TaskValidator(fields="__all__")]
