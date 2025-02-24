import datetime

from rest_framework.exceptions import ValidationError


class TaskValidator:
    """Валидатор для задач."""

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):

        # if not value.get('is_main_task'):
        #     if not value.get('parent_task'):
        #         raise ValidationError('У подзадачи необходимо указать родительскую задачу')

        if value.get("is_main_task"):
            if value.get("parent_task"):
                raise ValidationError("У основной задачи не может быть родительской задачи")

        date_now = datetime.date.today()
        if value.get("deadline") <= date_now:
            raise ValidationError("Срок выполнения не может быть назначен на сегодня или в прошлое")
