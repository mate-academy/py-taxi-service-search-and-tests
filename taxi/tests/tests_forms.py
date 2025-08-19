from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)


class FormsTests(TestCase):

    def test_driver_search_form_with_data(self):
        form = DriverSearchForm(data={"username": "test"})
        self.assertTrue(form.is_valid())

    def test_driver_search_form_empty(self):
        form = DriverSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())

    def test_car_search_form_with_data(self):
        form = CarSearchForm(data={"model": "Toyota"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_with_data(self):
        form = ManufacturerSearchForm(data={"name": "BMW"})
        self.assertTrue(form.is_valid())

    def test_validate_license_number_valid(self):
        valid_license = "ABC12345"
        result = validate_license_number(valid_license)
        self.assertEqual(result, valid_license)

    def test_validate_license_number_wrong_length(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("ABC123")
        self.assertIn("8 characters", str(context.exception))

    def test_validate_license_number_not_uppercase_letters(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("abc12345")
        self.assertIn("uppercase letters", str(context.exception))

    def test_validate_license_number_not_letters_first(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("12312345")
        self.assertIn("uppercase letters", str(context.exception))

    def test_validate_license_number_not_digits_last(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("ABCDEFGH")
        self.assertIn("digits", str(context.exception))

    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "testdriver",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "Driver"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license(self):
        form_data = {
            "username": "testdriver",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "abc123",
            "first_name": "Test",
            "last_name": "Driver"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_valid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "XYZ98765"})
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "invalid"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
