from django.urls import path

from task_tracker.apps import TaskTrackerConfig
from task_tracker.views import (TaskCreateAPIView, TaskDestroyAPIView,
                                TaskListAPIView, TaskRetrieveAPIView,
                                TaskUpdateAPIView)

app_name = TaskTrackerConfig.name

urlpatterns = [
    path("tasks/", TaskListAPIView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskRetrieveAPIView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateAPIView.as_view(), name="task-create"),
    path("tasks/update/<int:pk>/", TaskUpdateAPIView.as_view(), name="task-update"),
    path("tasks/delete/<int:pk>/", TaskDestroyAPIView.as_view(), name="task-delete"),
]
