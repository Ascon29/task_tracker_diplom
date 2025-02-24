from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from users.models import User
from users.permissions import IsAdmin
from users.serializers import UserCreateSerializer, UserSerializer


class UserCreateAPIView(CreateAPIView):
    """Контроллер создания пользователя."""

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    """Контроллер просмотра информации о пользователе."""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    """Контроллер обновления пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]


class UserListAPIView(ListAPIView):
    """Контроллер отображения списка пользователей, отсортированных по количеству активных задач."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = sorted(queryset, key=lambda x: x.task_set.filter(status="В работе").count(), reverse=True)
        return queryset


class UserDestroyAPIView(DestroyAPIView):
    """Контроллер удаления пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
