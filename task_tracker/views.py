from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from task_tracker.models import Task
from task_tracker.paginations import TaskPagination
from task_tracker.serializers import TaskSerializer


class TaskCreateAPIView(CreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskRetrieveAPIView(RetrieveAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskUpdateAPIView(UpdateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskListAPIView(ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    pagination_class = TaskPagination

    def get_queryset(self):
        return Task.objects.order_by("deadline")


class TaskDestroyAPIView(DestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
