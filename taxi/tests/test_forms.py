from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    validate_license_number,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm,
)


class DriverCreationFormTests(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class LicenseNumberValidationTests(TestCase):
    def test_license_number_valid(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_license_number_wrong_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC123")

    def test_license_number_first_three_not_uppercase_letters(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

    def test_license_number_last_five_not_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC123AB")


class SearchFormsTests(TestCase):
    def test_manufacturer_search_form_empty_value_is_valid(self):
        form = ManufacturerSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

    def test_car_search_form_empty_value_is_valid(self):
        form = CarSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())

    def test_driver_search_form_empty_value_is_valid(self):
        form = DriverSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())
