from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    CarForm,
    validate_license_number,
    DriverLicenseUpdateForm,
    DriverCreationForm
)

from taxi.models import Manufacturer


class CarFormTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="USA"
        )
        self.driver = get_user_model().objects.create_user(
            username="krixn",
            first_name="Serhii",
            last_name="Haiduchyk",
            password="1337"
        )

    def test_car_creation_form(self) -> None:
        form_data = {
            "model": "Honda",
            "manufacturer": self.manufacturer,
            "drivers": get_user_model().objects.all()
        }

        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestDriverForms(TestCase):
    def test_driver_creation_form_valid_license_number(self):
        data = {
            "username": "krixxxxn",
            "password1": "testpassword",
            "password2": "testpassword",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Wick",
        }
        form = DriverCreationForm(data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license_number_length(self):
        data = {
            "username": "krixxxxn",
            "password1": "111111",
            "password2": "111111",
            "license_number": "ABC1234",
            "first_name": "John",
            "last_name": "Wick",
        }
        form = DriverCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_valid_license_number(self):
        data = {"license_number": "QWE22888"}
        form = DriverLicenseUpdateForm(data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid_license_number_format(self):
        data = {"license_number": "1337QWE"}
        form = DriverLicenseUpdateForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_validate_license_number_valid(self):
        license_number = "QWE22788"
        self.assertEqual(
            validate_license_number(license_number),
            license_number
        )

    def test_validate_license_number_invalid_length(self):
        license_number = "QWE1111"
        with self.assertRaises(ValidationError):
            validate_license_number(license_number)
