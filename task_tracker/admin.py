from django.contrib import admin

from task_tracker.models import Task
from users.models import User


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "is_main_task", "parent_task", "deadline", "status"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "full_name", "job_title"]
