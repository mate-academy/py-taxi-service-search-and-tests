from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, validate_license_number


class FormsTests(TestCase):
    def test_driver_creation_form_with_attributes_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TES12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TES12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class LicenseNumberValidationTests(TestCase):
    def test_right_license_number(self):
        license_number = "TES12345"
        self.assertEqual(
            license_number,
            validate_license_number(license_number)
        )

    def test_license_number_with_wrong_length(self):
        license_number = "TES1234"
        license_number_ = "TES1234567"
        error_message = "License number should consist of 8 characters"
        with self.assertRaisesMessage(ValidationError, error_message):
            validate_license_number(license_number)
            validate_license_number(license_number_)

    def test_first_3_uppercase(self):
        license_number = "tes12345"
        license_number_ = "12345678"
        error_message = "First 3 characters should be uppercase letters"
        with self.assertRaisesMessage(ValidationError, error_message):
            validate_license_number(license_number)
            validate_license_number(license_number_)

    def test_last_5_are_digits(self):
        license_number = "TEST1234"
        license_number_ = "TESTTSET"
        error_message = "Last 5 characters should be digits"
        with self.assertRaisesMessage(ValidationError, error_message):
            validate_license_number(license_number)
            validate_license_number(license_number_)
