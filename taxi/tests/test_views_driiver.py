from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver

DRIVERS_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(DRIVERS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        get_user_model().objects.create_user(
            username="blin4ik",
            password="test12345",
            first_name="Vlad",
            last_name="Magdenko",
            license_number="ABC12345"
        )

        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]),
                         list(Driver.objects.all()))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_create(self):
        form_data = {
            "username": "user_test",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "test",
            "last_name": "test",
            "license_number": "ABC12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(new_driver.license_number, form_data["license_number"])
