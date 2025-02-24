from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from task_tracker.models import Task
from users.models import User


class TaskTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@mail.ru", password=123, job_title="test_title", full_name="test_name"
        )
        self.user.is_superuser = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(name="test_task", deadline="2026-10-10", is_main_task=True)
        self.task.executor.set([self.user.id])
        self.task.save()

    def test_task_create(self):
        url = reverse("task_tracker:task-create")
        data = {"name": "test_create", "deadline": "2026-02-02", "is_main_task": True, "executor": [self.user.id]}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_task_retrieve(self):
        url = reverse("task_tracker:task-detail", args=(self.task.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("id"), self.task.pk)

    def test_task_update(self):
        url = reverse("task_tracker:task-update", args=(self.task.pk,))
        data = {"name": "test_update", "deadline": "2026-10-10"}
        response = self.client.patch(url, data)
        new_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_data.get("name"), data.get("name"))

    def test_task_list(self):
        url = reverse("task_tracker:task-list")
        response = self.client.get(url)
        data = response.json().get("results")[0]
        result = {
            "id": self.task.id,
            "name": self.task.name,
            "description": self.task.description,
            "is_main_task": self.task.is_main_task,
            "deadline": self.task.deadline,
            "status": self.task.status,
            "executor": [6],
            "parent_task": self.task.parent_task,
        }
        # print(data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_task_delete(self):
        url = reverse("task_tracker:task-delete", args=(self.task.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_start_task(self):
        url = reverse("task_tracker:task-start", args=(self.task.pk,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complete_task(self):
        url = reverse("task_tracker:task-complete", args=(self.task.pk,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_end_task(self):
        url = reverse("task_tracker:task-end", args=(self.task.pk,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
