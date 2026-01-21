from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number
)
from taxi.models import Manufacturer


DRIVERS_DATA = {
    "username": "test",
    "license_number": "ABC12345",
    "password1": "Test1234q",
    "password2": "Test1234q"
}


class CarFormTest(TestCase):

    def test_car_form_valid_creation(self):
        manufacturer = Manufacturer.objects.create(
            name="test123",
            country="Germany"
        )

        user = get_user_model().objects.create_user(
            username="test_username",
            license_number="ABC12346",
            password="Test1234q",

        )

        form_data = {
            "model": "model_test",
            "manufacturer": manufacturer.id,
            "drivers": [user.id, ]
        }

        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid_creation(self):
        form_data = {
            "model": "model_test"
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverFormTest(TestCase):

    def test_driver_form_valid_creation(self):
        form = DriverCreationForm(data=DRIVERS_DATA)
        self.assertTrue(form.is_valid())

    def test_driver_form_invalid_creation(self):
        form_data = {
            "username": "model_test"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_valid(self):
        form = DriverLicenseUpdateForm(data={
            "license_number": "ABC12345",
        })
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid(self):
        form = DriverLicenseUpdateForm(data={
            "license_number": "abc12345",
        })
        self.assertFalse(form.is_valid())


class ValidateLicenseNumberTest(TestCase):
    def test_valid_license_number(self):
        valid_license_number = "ABC12345"
        self.assertEqual(
            validate_license_number(valid_license_number),
            valid_license_number
        )

    def test_invalid_length(self):
        invalid_license_number = "ABC123"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_first_characters(self):
        invalid_license_number = "abc12345"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_last_characters(self):
        invalid_license_number = "ABCxyz12"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)
