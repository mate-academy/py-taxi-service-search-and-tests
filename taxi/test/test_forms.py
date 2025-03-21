from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Car, Manufacturer
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
    validate_license_number
)
from django.core.exceptions import ValidationError


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan")
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="test123",
            license_number="ABC12345")
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="test123",
            license_number="XYZ67890")

    def test_valid_car_form(self):
        form_data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_car_form_empty_drivers(self):
        form_data = {
            "model": "Corolla",
            "manufacturer": self.manufacturer.id,
            "drivers": []
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("drivers", form.errors)


class DriverCreationFormTest(TestCase):
    def test_valid_driver_creation_form(self):
        form_data = {
            "username": "testuser",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "XYZ12345",
            "first_name": "John",
            "last_name": "Doe"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_driver_creation_form_license_number(self):
        form_data = {
            "username": "testuser",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "123XYZ",  # Invalid format
            "first_name": "John",
            "last_name": "Doe"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(TestCase):
    def test_valid_license_update(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())

    def test_invalid_license_update(self):
        form = DriverLicenseUpdateForm(data={"license_number": "12345XYZ"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class LicenseNumberValidationTest(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(validate_license_number("XYZ12345"), "XYZ12345")

    def test_invalid_license_number_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("XYZ1234")  # Only 7 characters

    def test_invalid_license_number_uppercase(self):
        with self.assertRaises(ValidationError):
            validate_license_number("xyz12345")  # Lowercase letters

    def test_invalid_license_number_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("XYZABCDE")  # No digits


class SearchFormsTest(TestCase):
    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "testdriver"})
        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "Camry"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())
