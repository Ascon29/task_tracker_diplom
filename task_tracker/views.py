from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from config import settings
from task_tracker.models import Task
from task_tracker.paginations import TaskPagination
from task_tracker.serializers import TaskSerializer
from users.permissions import IsAdmin, IsExecutor


class TaskCreateAPIView(CreateAPIView):
    """Контроллер создания задачи."""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAdmin]


class TaskRetrieveAPIView(RetrieveAPIView):
    """Контроллер просмотра информации о задаче."""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAdmin | IsExecutor]


class TaskUpdateAPIView(UpdateAPIView):
    """Контроллер обновления задачи."""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAdmin]


class TaskListAPIView(ListAPIView):
    """Контроллер просмотра списка задач."""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    pagination_class = TaskPagination
    permission_classes = [IsAdmin | IsAuthenticated]

    def get_queryset(self):
        """Сортировка по сроку (первые отображаются задачи, у которых заканчивается срок в ближайшее время).
        Начальник (суперпользователь) видит все задачи. Сотрудник (исполнитель) видит только назначенные ему задачи."""
        if self.request.user.is_superuser:
            return Task.objects.order_by("deadline")
        else:
            return Task.objects.order_by("deadline").filter(executor=self.request.user)


class TaskDestroyAPIView(DestroyAPIView):
    """Контроллер удаления задачи."""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAdmin]


class StartTaskAPIView(APIView):
    """Контроллер запуска задачи в работу или возврата на доработку, в зависимости от статуса задачи.
    Происходит отправка уведомлений исполнителям на email. Устанавливает статус задачи: 'В работе'."""

    permission_classes = [IsAdmin]

    def post(self, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs["pk"])
        subject = f"Треккер задач {settings.COMPANY_NAME}"

        # Сообщение, если статус задачи "Создана"
        if Task.CREATED:
            message = f"Вам поставлена задача: {task.name}, срок выполнения: {task.deadline}.\n Для подробной информации о задаче перейдите по ссылке: {settings.APP_ROOT}{task.id}/"
        # Сообщение, если статус задачи "На проверке"
        elif Task.VERIFICATION:
            message = f"Задача '{task.name}' возвращена на доработку!\n Для подробной информации о задаче перейдите по ссылке: {settings.APP_ROOT}{task.id}/"

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [executor.email for executor in task.executor.all()]

        for recipient in recipient_list:
            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    [recipient],
                )
                task.status = Task.AT_WORK
                task.save()
                return HttpResponse(f"Уведомление о задаче '{task.name}' отправлено.")
            except Exception as e:
                return HttpResponse(f"При отправке сообщения произошла ошибка: {e}")


class CompleteTaskAPIView(APIView):
    """Контроллер завершения задачи. Устанавливает статус задачи: 'Завершена'."""

    permission_classes = [IsAdmin]

    def post(self, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs["pk"])
        task.status = Task.COMPLETED
        task.save()
        return HttpResponse(f"Задача '{task.name}' успешно выполнена")


class EndTaskAPIView(APIView):
    """Контроллер для сдачи задачи на проверку. Устанавливает статус задачи: 'На проверке'."""

    permission_classes = [IsExecutor]

    def post(self, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs["pk"])
        task.status = Task.VERIFICATION
        task.save()
        return HttpResponse(f"Задача '{task.name}' сдана на проверку")


class ImportantTask(APIView):

    def get(self, *args, **kwargs):

        important_tasks = Task.objects.filter(status="Создана", parent_task__status="В работе")
        print(important_tasks)
        return HttpResponse("")
