from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm


class FormTest(TestCase):
    def test_driver_creation_form(self):
        data = {
            "username": "john.smith",
            "password1": "HardPassword!1",
            "password2": "HardPassword!1",
            "first_name": "John",
            "last_name": "Smith",
            "license_number": "AAA11111",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Mykyta",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        data = {
            "username": "john.smith",
            "password1": "HardPassword!1",
            "password2": "HardPassword!1",
            "first_name": "John",
            "last_name": "Smith",
            "license_number": "AAA11111",
        }
        self.client.post(reverse("taxi:driver-create"), data)
        new_user = get_user_model().objects.get(username=data["username"])

        self.assertEqual(new_user.first_name, data["first_name"])
        self.assertEqual(new_user.last_name, data["last_name"])
        self.assertEqual(new_user.license_number, data["license_number"])
