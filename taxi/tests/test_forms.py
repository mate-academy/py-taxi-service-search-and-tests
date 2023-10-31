from django.core.exceptions import ValidationError
from django.test import TestCase

from ..forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number
)
from ..models import Driver


class DriverFormTests(TestCase):
    def test_validate_license_number_valid(self):
        valid_license = "ABC12345"
        self.assertEqual(validate_license_number(valid_license), valid_license)

    def test_validate_license_number_invalid_length(self):
        invalid_license = "AB12"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license)

    def test_validate_license_number_invalid_format(self):
        invalid_license = "abc12345"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license)

    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "testuser",
            "password1": "testing321",
            "password2": "testing321",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid(self):
        form_data = {
            "username": "testuser",
            "password1": "testing321",
            "password2": "testing123",  # Different password
            "license_number": "invalid",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_update_form_valid(self):
        driver = Driver.objects.create(license_number="ABC12345")
        form_data = {"license_number": "ABC54321"}
        form = DriverLicenseUpdateForm(data=form_data, instance=driver)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        driver = Driver.objects.create(license_number="ABC12345")
        form_data = {"license_number": "invalid"}
        form = DriverLicenseUpdateForm(data=form_data, instance=driver)
        self.assertFalse(form.is_valid())
