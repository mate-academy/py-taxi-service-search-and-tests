from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_LIST_URL: str = reverse("taxi:driver-list")


class PublicDriverListViewTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 302)


class PrivateDriverListViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="TestPassword123",
            license_number="TEST12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_list(self) -> None:
        driver1 = Driver.objects.create(
            username="driver1",
            password="TestPassword123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        driver2 = Driver.objects.create(
            username="driver2",
            password="TestPassword123",
            first_name="Jane",
            last_name="Smith",
            license_number="ABC54321"
        )

        response = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            # Проверяем, что в списке нужные объекты
            set(response.context["driver_list"]),
            # Используем множество для сравнения, так как порядок не важен
            set([self.user, driver1, driver2])
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_by_username(self) -> None:
        Driver.objects.create(
            username="john",
            password="TestPassword123",
            first_name="John",
            last_name="Doe",
            license_number="LICENSE1"
        )
        Driver.objects.create(
            username="jane",
            password="TestPassword123",
            first_name="Jane",
            last_name="Smith",
            license_number="LICENSE2"
        )

        response = self.client.get(DRIVER_LIST_URL, {"username": "jan"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        # Проверяем, что первый элемент содержит искомую подстроку
        self.assertIn(
            "jan",
            response.context["driver_list"][0].username
        )

    def test_search_by_nonexistent_username(self) -> None:
        Driver.objects.create(
            username="john",
            password="TestPassword123",
            first_name="John",
            last_name="Doe",
            license_number="LICENSE1"
        )

        response = self.client.get(DRIVER_LIST_URL, {"username": "xyz"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 0)
