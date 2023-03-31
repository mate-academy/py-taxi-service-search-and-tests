from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver


class PrivateCreateDriver(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "pass123")
        self.client.force_login(self.user)

    def test_create_driver(self):
        form = {
            "username": "Username",
            "password1": "passworD123!@#",
            "password2": "passworD123!@#",
            "license_number": "ADS35321",
            "first_name": "First",
            "last_name": "Last",
        }
        self.client.post(reverse("taxi:driver-create"), data=form)
        new_user = get_user_model().objects.get(
            license_number=form["license_number"]
        )

        self.assertEqual(
            new_user.license_number, form["license_number"]
        )
        self.assertEqual(
            new_user.first_name, form["first_name"]
        )
        self.assertEqual(
            new_user.last_name, form["last_name"]
        )
