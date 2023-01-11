from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_is_valid(self):
        form_data = {
            "username": "user_name",
            "password1": "3134test",
            "password2": "3134test",
            "first_name": "first name",
            "last_name": "last name",
            "license_number": "UAQ12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_number_has_two_letters(self):
        form_data = {
            "username": "user_name",
            "password1": "3134test",
            "password2": "3134test",
            "first_name": "first name",
            "last_name": "last name",
            "license_number": "UA123456"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_number_is_too_long(self):
        form_data = {
            "username": "user_name",
            "password1": "3134test",
            "password2": "3134test",
            "first_name": "first name",
            "last_name": "last name",
            "license_number": "UAQ123456"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_number_is_lowercase(self):
        form_data = {
            "username": "user_name",
            "password1": "3134test",
            "password2": "3134test",
            "first_name": "first name",
            "last_name": "last name",
            "license_number": "uaq123456"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_number_is_too_short(self):
        form_data = {
            "username": "user_name",
            "password1": "3134test",
            "password2": "3134test",
            "first_name": "first name",
            "last_name": "last name",
            "license_number": "UAQ1234"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "user_name",
            "password1": "3134test",
            "password2": "3134test",
            "first_name": "first name",
            "last_name": "last name",
            "license_number": "UAQ12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
