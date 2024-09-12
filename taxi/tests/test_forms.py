from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number,
)

from taxi.models import Car, Manufacturer


class CarFormTests(TestCase):
    def setUp(self):
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            license_number="ABC12345",
            password="password123"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            license_number="DEF67890",
            password="password123"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="TestManufacturer"
        )
        self.car = Car.objects.create(
            model="TestModel",
            manufacturer=self.manufacturer
        )

    def test_car_form_valid_data(self):
        form_data = {
            "model": "TestModel",
            "manufacturer": self.manufacturer,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid_data(self):
        form_data = {
            "model": "",
            "manufacturer": self.manufacturer,
            "drivers": [self.driver1.id],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverCreationFormTests(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "test_driver",
            "password1": "test_password123",
            "password2": "test_password123",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "Driver",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license(self):
        form_data = {
            "username": "test_driver",
            "password1": "test_password123",
            "password2": "test_password123",
            "license_number": "123ABC45",
            "first_name": "Test",
            "last_name": "Driver",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            license_number="ABC12345",
            password="password123"
        )

    def test_license_update_form_valid(self):
        form_data = {"license_number": "XYZ67890"}
        form = DriverLicenseUpdateForm(instance=self.driver, data=form_data)
        self.assertTrue(form.is_valid())

    def test_license_update_form_invalid(self):
        form_data = {"license_number": "invalid"}
        form = DriverLicenseUpdateForm(instance=self.driver, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class LicenseNumberValidationTests(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_invalid_license_number_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234")

    def test_invalid_license_number_letters(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

    def test_invalid_license_number_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC12XYZ")
