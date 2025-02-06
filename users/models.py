from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name="E-mail адрес", help_text="Введите свой E-mail")
    job_title = models.CharField(max_length=100, verbose_name="Должность", help_text="Введите должность")
    full_name = models.CharField(max_length=100, verbose_name="ФИО", help_text="Введите фамилию, имя и отчество")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.email
