from rest_framework import pagination


class TaskPagination(pagination.PageNumberPagination):
    """Пагинация для списка задач."""

    page_size = 5
