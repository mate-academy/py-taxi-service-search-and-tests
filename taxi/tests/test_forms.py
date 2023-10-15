from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverSearchForm, DriverCreationForm


class TestDriverUsernameSearchForm(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin",
        )
        self.client.force_login(self.user)
        get_user_model().objects.create_user(
            username="johnson",
            password="johnson",
            license_number="BON26231",
        )
        get_user_model().objects.create_user(
            username="john",
            password="john",
            license_number="ION26232",
        )

    def test_driver_username_search_form(self):
        form_data = {"username": "admin"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_username_search_form_username_search(self):
        form_data = {"username": "john"}
        url = reverse("taxi:driver-list")
        response = self.client.get(url, data=form_data)
        self.assertContains(response, form_data["username"])
        self.assertNotContains(response, "johnson")


class TestDriverCreationForm(TestCase):
    def test_driver_creation_form_with_valid_license_number(self):
        form_data = {
            "username": "admin",
            "password1": "123456",
            "password2": "123456",
            "license_number": "JON26231",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_without_license_number(self):
        form_data = {
            "username": "admin",
            "password1": "123456",
            "password2": "123456",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_license_number_too_short(self):
        form_data = {
            "username": "admin",
            "password1": "123456",
            "password2": "123456",
            "license_number": "JON2623",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_license_number_too_long(self):
        form_data = {
            "username": "admin",
            "password1": "123456",
            "password2": "123456",
            "license_number": "JON262334",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_license_number_with_only_digits(self):
        form_data = {
            "username": "admin",
            "password1": "123456",
            "password2": "123456",
            "license_number": "12345678",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_license_number_with_only_letters(self):
        form_data = {
            "username": "admin",
            "password1": "123456",
            "password2": "123456",
            "license_number": "ABCDEFGHI",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
