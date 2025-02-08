from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда для создания суперпользователя"""

    def handle(self, *args, **options):
        user = User.objects.create(email="admin@example.com")
        user.set_password("123")
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
