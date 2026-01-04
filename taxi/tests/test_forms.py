from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    validate_license_number,
    DriverCreationForm,
    DriverLicenseUpdateForm,
)
from taxi.models import Driver


class LicenseNumberValidationTests(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(
            validate_license_number("ABC12345"),
            "ABC12345"
        )

    def test_invalid_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC123")

    def test_invalid_first_three_chars(self):
        with self.assertRaises(ValidationError):
            validate_license_number("AbC12345")

    def test_invalid_last_five_chars(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC12A45")


class DriverCreationFormTests(TestCase):
    def test_form_valid_data(self):
        form = DriverCreationForm(data={
            "username": "driver1",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_license(self):
        form = DriverCreationForm(data={
            "username": "driver1",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "abc12345",
            "first_name": "John",
            "last_name": "Doe",
        })
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="driver2",
            password="pass12345",
            license_number="ABC12345"
        )

    def test_update_valid_license(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "XYZ67890"},
            instance=self.driver
        )
        self.assertTrue(form.is_valid())

    def test_update_invalid_license(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "xyz67890"},
            instance=self.driver
        )
        self.assertFalse(form.is_valid())
