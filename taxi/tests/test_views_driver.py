from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        get_user_model().objects.create_user(
            username="mil.snake",
            password="password123",
            first_name="Milly",
            last_name="Snaider",
            license_number="sdfkds34352333"
        )

        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")
