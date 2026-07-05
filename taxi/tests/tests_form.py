from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    validate_license_number,
    DriverLicenseUpdateForm,
    DriverCreationForm,
    CarForm
)
from taxi.models import Manufacturer


class TestForms(TestCase):
    def test_validate_license_number_with_valid_data(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_validate_license_number_with_incorrect_length(self):
        self.assertRaises(
            ValidationError,
            validate_license_number,
            "ABC123456"
        )

    def test_validate_license_number_with_incorrect_prefix(self):
        self.assertRaises(
            ValidationError,
            validate_license_number,
            "abc12345"
        )

    def test_validate_license_number_with_incorrect_suffix(self):
        self.assertRaises(
            ValidationError,
            validate_license_number,
            "ABC12f45"
        )

    def test_driver_update_license_number_with_correct_data(self):
        form_data = {"license_number": "TES12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_update_license_number_with_incorrect_data(self):
        form_data = {"license_number": "ABC123456"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"]
        )

    def test_driver_creation_form_with_invalid_license_number(self):
        form_data = {
            "username": "Test User",
            "password1": "Test Password",
            "password2": "Test Password",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "TE012356"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"]
        )

    def test_car_form_with_valid_data(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Factory",
            country="Test Country"
        )
        driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="password123",
            license_number="DRV12345"
        )
        driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="password123",
            license_number="DRV67890"
        )
        form_data = {
            "model": "Test Car Model",
            "manufacturer": manufacturer.id,
            "drivers": [driver1.id, driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        car = form.save()
        self.assertEqual(car.drivers.count(), 2)
