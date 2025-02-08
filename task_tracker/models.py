from django.db import models

from config import settings


class Task(models.Model):
    """Модель задач для сотрудников."""

    CREATED = "Создана"
    AT_WORK = "В работе"
    VERIFICATION = "На проверке"
    COMPLETED = "Завершена"
    STATUS_CHOICES = (
        (CREATED, "Создана"),
        (AT_WORK, "В работе"),
        (VERIFICATION, "На проверке"),
        (COMPLETED, "Завершена"),
    )

    name = models.CharField(max_length=255, unique=True, verbose_name="Задача", help_text="Введите название задачи")
    description = models.TextField(
        verbose_name="Описание задачи", help_text="Ведите подробное описание задачи", blank=True, null=True
    )
    is_main_task = models.BooleanField(
        default=False,
        verbose_name="Признак основной задачи",
        help_text="Укажите, эта задача является основной или подзадачей",
    )
    parent_task = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Родительская задача",
        help_text="Укажите родительскую задачу",
        blank=True,
        null=True,
    )
    executor = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name="Исполнитель(ли)", help_text="Выберите исполнителя(лей)"
    )
    deadline = models.DateField(verbose_name="Срок выполнения", help_text="Введите крайний срок выполнения задачи")
    status = models.CharField(choices=STATUS_CHOICES, default=CREATED, verbose_name="Статус задачи")

    def __str__(self):
        return f"{self.name}, срок выполнения: {self.deadline}"

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["deadline"]
