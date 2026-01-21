from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.forms import DriverCreationForm, validate_license_number


class DriverFormsTests(TestCase):
    def setUp(self):
        pass

    def test_driver_creation_with_license_first_name_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "license_number": "SSD12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
        self.assertEqual(form.cleaned_data.get("license_number"), "SSD12345")


class PrivateAuthorTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "license_number": "SSD12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class ValidateLicenseNumberTests(TestCase):

    def test_valid_license_number(self):
        try:
            validate_license_number("ABC12345")
        except ValidationError:
            self.fail(
                "validate_license_number raised ValidationError unexpectedly!"
            )

    def test_invalid_length(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("AB1234")
        exception = context.exception
        self.assertEqual(
            exception.message, "License number should consist of 8 characters"
        )

    def test_invalid_prefix(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("abC12345")
        exception = context.exception
        self.assertEqual(
            exception.message, "First 3 characters should be uppercase letters"
        )

    def test_invalid_suffix(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("ABC12ABC")
        exception = context.exception
        self.assertEqual(
            exception.message,
            "Last 5 characters should be digits"
        )

    def test_invalid_characters(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("ABC12AB!")
        exception = context.exception
        self.assertEqual(
            exception.message,
            "Last 5 characters should be digits"
        )
