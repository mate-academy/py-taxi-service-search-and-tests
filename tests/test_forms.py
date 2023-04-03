from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (DriverSearchForm,
                        CarSearchForm,
                        ManufacturerSearchForm,
                        DriverCreationForm,
                        DriverLicenseUpdateForm,
                        validate_license_number)


class TestSearchForms(TestCase):
    def test_driver_search_form(self):
        form_data = {"username": "johndoe"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_search_form(self):
        form_data = {"model": "Toyota Camry"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form(self):
        form_data = {"name": "Toyota"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverCreationFormTestCase(TestCase):
    def setUp(self):
        self.valid_data = {
            "username": "johndoe",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "user12345",
            "password2": "user12345",
        }
        self.invalid_data = [
            {
                "username": "johndoe",
                "license_number": "ABCD12345",
                "first_name": "John",
                "last_name": "Doe",
                "password1": "mypassword",
                "password2": "mypassword",
                "error_message": "License number should "
                                 "consist of 8 characters",
            },
            {
                "license_number": "abc12345",
                "error_message": "First 3 characters should "
                                 "be uppercase letters",
            },
            {
                "license_number": "ABC12X45",
                "error_message": "Last 5 characters "
                                 "should be digits",
            },
        ]

    def test_valid_license_number(self):
        form = DriverCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

        form = DriverLicenseUpdateForm(
            data={"license_number": self.valid_data["license_number"]}
        )
        self.assertTrue(form.is_valid())

    def test_invalid_license_number(self):
        for data in self.invalid_data:
            form = DriverCreationForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertIn(data["error_message"], form.errors["license_number"])

            form = DriverLicenseUpdateForm(
                data={"license_number": data["license_number"]}
            )
            self.assertFalse(form.is_valid())
            self.assertIn(data["error_message"], form.errors["license_number"])


class ValidateLicenseNumberTest(TestCase):
    def test_valid_license_number(self):
        valid_license_number = "ABC12345"
        result = validate_license_number(valid_license_number)
        self.assertEqual(result, valid_license_number)

    def test_invalid_license_number(self):
        invalid_license_number = "123ABCD"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_license_number_length(self):
        invalid_license_number = "ABCD123"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_license_number_first_three_characters(self):
        invalid_license_number = "abc12345"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_license_number_last_five_characters(self):
        invalid_license_number = "ABC12D45"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)
