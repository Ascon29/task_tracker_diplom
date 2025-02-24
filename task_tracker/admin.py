from django.contrib import admin

from task_tracker.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "is_main_task", "parent_task", "deadline", "status"]
