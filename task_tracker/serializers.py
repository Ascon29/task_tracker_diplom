from rest_framework import serializers

from task_tracker.models import Task
from task_tracker.validators import TaskValidator


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор для задач."""

    class Meta:
        model = Task
        fields = ["id", "name", "description", "is_main_task", "deadline", "status", "executor", "parent_task"]
        validators = [TaskValidator(fields="__all__")]
