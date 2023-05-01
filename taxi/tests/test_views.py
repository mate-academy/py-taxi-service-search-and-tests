from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver


DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test username",
            password="test1234",
            license_number="TST12345"
        )
        self.client.force_login(self.user)

        Driver.objects.create(
            username="driver1",
            password="password1",
            license_number="ABC12345",
        )
        Driver.objects.create(
            username="driver2",
            password="password2",
            license_number="ZXC!@#$%",
        )

    def test_create_driver(self):
        form_data = {
            "username": "new.user",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "TST12346"
        }

        self.client.post(DRIVER_CREATE_URL, data=form_data)

        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_LIST_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")
