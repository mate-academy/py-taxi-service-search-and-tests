from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

DRIVERS_URL = reverse("taxi:driver-list")


class PublicDriverViewTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVERS_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test username",
            password="Test password",
            license_number="Test number"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        get_user_model().objects.create_user(
            username="Test second username",
            password="Test second password",
            license_number="Test second number"
        )

        response = self.client.get(DRIVERS_URL)
        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
