from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    """Контроллер создания пользователя."""

    serializer_class = UserSerializer
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


class UserListAPIView(ListAPIView):
    """Контроллер отображения списка пользователей."""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    """Контроллер удаления пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
