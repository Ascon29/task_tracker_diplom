from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@mail.ru", password=123, job_title="test_title", full_name="test_name"
        )
        self.user.is_superuser = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        """Тест создания пользователя."""
        url = reverse("users:register")
        data = {
            "email": "test@register.ru",
            "password": 123,
            "job_title": "test_register",
            "full_name": "test_register",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

        wrong_data = {"email": "", "password": 123, "job_title": "test_title", "full_name": "test_name"}
        wrong_response = self.client.post(url, wrong_data)
        self.assertEqual(wrong_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_retrieve(self):
        """Тест просмотра информации о пользователе."""
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("id"), self.user.pk)

    def test_user_update(self):
        """Тест обновления информации о пользователе."""
        url = reverse("users:user-update", args=(self.user.pk,))
        data = {"job_title": "test_update", "full_name": "test_update"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_delete(self):
        """Тест удаления пользователя."""
        url = reverse("users:user-delete", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)

    def test_user_list(self):
        """Тест просмотра списка пользователей."""
        url = reverse("users:user-list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.user.pk,
                "email": self.user.email,
                "full_name": self.user.full_name,
                "job_title": self.user.job_title,
                "active_tasks": [],
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
