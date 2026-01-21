from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "test_username",
            "license_number": "TES12345",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "test_password_123",
            "password2": "test_password_123",
        }

    def test_driver_creation_form(self) -> None:
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_create_driver(self) -> None:
        self.user = get_user_model().objects.create_user(
            username=self.form_data.get("username"),
            password=self.form_data.get("password1"),
            license_number=self.form_data.get("license_number"),
            first_name=self.form_data.get("first_name"),
            last_name=self.form_data.get("last_name")
        )
        self.client.force_login(self.user)
        self.client.post(
            reverse("taxi:driver-create"),
            data=self.form_data
        )
        new_user = get_user_model().objects.get(
            username=self.form_data.get("username")
        )

        self.assertEqual(
            new_user.first_name,
            self.form_data.get("first_name")
        )
        self.assertEqual(
            new_user.last_name,
            self.form_data.get("last_name")
        )
        self.assertEqual(
            new_user.license_number,
            self.form_data.get("license_number")
        )
