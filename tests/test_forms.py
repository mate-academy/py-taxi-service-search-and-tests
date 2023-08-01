from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Car


class FormsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )

        self.client.force_login(self.user)

    def test_driver_creation_is_valid(self):
        form_data = {
            "username": "new_driver",
            "password1": "driver12345",
            "password2": "driver12345",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "ABC12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(
            new_driver.username,
            form_data["username"]
        )
        self.assertEqual(
            new_driver.first_name,
            form_data["first_name"]
        )
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )
