from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer
from taxi.forms import (
    CarForm,
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm, 
    validate_license_number,
)


class TaxiFormsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="manufacturer_name", country="manufacturer_country"
        )

    def test_car_form_valid(self):
        form_data = {
            "model": "Test Model",
            "manufacturer": self.manufacturer,
            "drivers": [self.user.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self):
        form_data = {
            "model": "",
            "manufacturer": self.manufacturer,
            "drivers": [self.user.id],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_car_search_form_valid(self):
        form_data = {"model": "Test Model"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form_invalid(self):
        form_data = {"model": ""}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_valid(self):
        form_data = {"username": "test_user"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_invalid(self):
        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_valid(self):
        form_data = {"name": "Test Manufacturer"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_invalid(self):
        form_data = {"name": ""}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "newpassword",
            "password2": "newpassword",
            "license_number": "ABC23456",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_invalid(self):
        form_data = {
            "username": "",
            "password1": "newpassword",
            "password2": "newpassword",
            "license_number": "AB123456",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_update_form_valid(self):
        form_data = {"license_number": "ABC23456"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        form_data = {"license_number": "invalid"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestValidateLicenseNumber(TestCase):

    def test_valid_license_number(self):
        valid_license_number = "ABC12345"
        result = validate_license_number(valid_license_number)
        self.assertEqual(result, valid_license_number)

    def test_invalid_length(self):
        invalid_license_number = "ABCDE"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_first_three_characters(self):
        invalid_license_number = "12313265"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_last_five_characters(self):
        invalid_license_number = "ABC1234X"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_case(self):
        invalid_license_number = "abc12345"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_all_letters(self):
        invalid_license_number = "ABCabcde"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_overlenght(self):
        invalid_license_number = "ABC123456"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_characters(self):
        invalid_license_number = "!@#$%^&*"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)
