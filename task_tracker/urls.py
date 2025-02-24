from django.urls import path

from task_tracker.apps import TaskTrackerConfig
from task_tracker.views import (CompleteTaskAPIView, EndTaskAPIView,
                                ImportantTask, StartTaskAPIView,
                                TaskCreateAPIView, TaskDestroyAPIView,
                                TaskListAPIView, TaskRetrieveAPIView,
                                TaskUpdateAPIView)

app_name = TaskTrackerConfig.name

urlpatterns = [
    path("tasks/", TaskListAPIView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskRetrieveAPIView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateAPIView.as_view(), name="task-create"),
    path("tasks/update/<int:pk>/", TaskUpdateAPIView.as_view(), name="task-update"),
    path("tasks/delete/<int:pk>/", TaskDestroyAPIView.as_view(), name="task-delete"),
    path("start_task/<int:pk>/", StartTaskAPIView.as_view(), name="task-start"),
    path("complete_task/<int:pk>/", CompleteTaskAPIView.as_view(), name="task-complete"),
    path("end_task/<int:pk>/", EndTaskAPIView.as_view(), name="task-end"),
    path("important_task/", ImportantTask.as_view(), name="important-task"),
]
