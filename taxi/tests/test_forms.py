from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        CarSearchForm,
                        ManufacturerSearchForm,
                        DriverSearchForm,
                        validate_license_number)


class DriverCreateFormTests(TestCase):
    def test_create_driver_with_valid_data(self):
        user_data = {
            "username": "test_username",
            "password1": "Test12345",
            "password2": "Test12345",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "AAA12345",
        }
        form = DriverCreationForm(data=user_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, user_data)

    def test_create_driver_with_invalid_license_number(self):
        user_data = {
            "username": "test_username",
            "password1": "Test12345",
            "password2": "Test12345",
            "license_number": "A1234",
        }
        form = DriverCreationForm(data=user_data)
        self.assertFalse(form.is_valid())


class DriverSearchFormTest(TestCase):
    def test_model_field_present(self):
        field = "username"
        form_data = {field: "test_model"}
        form = DriverSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)


class ValidLicenseNumberFormTest(TestCase):
    def test_validation_license_number_with_valid_data(self):
        self.assertEqual(validate_license_number("AAA12345"), "AAA12345")

    def test_length_of_license_number_should_be_not_more_than_8(self):
        self.assertRaises(
            ValidationError,
            validate_license_number,
            "AAA123456"
        )

    def test_length_of_license_number_should_be_not_less_than_8(self):
        self.assertRaises(ValidationError, validate_license_number, "AAA123")

    def test_first_3_characters_should_be_uppercase_letters(self):
        self.assertRaises(ValidationError, validate_license_number, "TE123456")

    def test_last_5_characters_should_be_be_digits(self):
        self.assertRaises(ValidationError, validate_license_number, "TEST2345")


class CarSearchFormTest(TestCase):
    def test_model_field_present(self):
        field = "model"
        form_data = {field: "test_model"}
        form = CarSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)


class ManufacturerSearchFormTest(TestCase):
    def test_model_field_present(self):
        field = "name"
        form_data = {field: "test_model"}
        form = ManufacturerSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)
