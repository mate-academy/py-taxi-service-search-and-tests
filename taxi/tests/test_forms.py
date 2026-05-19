from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarForm,
    ManufacturerSearchForm,
    DriverSearchForm,
    CarSearchForm,
)
from taxi.models import Manufacturer, Car


class LicenseNumberValidationTest(TestCase):
    """Tests for validate_license_number used in both driver forms."""

    def test_valid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())

    def test_license_too_short(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC1234"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_too_long(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC123456"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_first_3_not_uppercase(self):
        form = DriverLicenseUpdateForm(data={"license_number": "abc12345"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_first_3_not_alpha(self):
        form = DriverLicenseUpdateForm(data={"license_number": "12312345"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_last_5_not_digits(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABCDEFGH"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverCreationFormTest(TestCase):
    def test_valid_form(self):
        form = DriverCreationForm(
            data={
                "username": "testdriver",
                "password1": "strong_pass_123",
                "password2": "strong_pass_123",
                "first_name": "John",
                "last_name": "Doe",
                "license_number": "ABC12345",
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_license_in_creation_form(self):
        form = DriverCreationForm(
            data={
                "username": "testdriver",
                "password1": "strong_pass_123",
                "password2": "strong_pass_123",
                "first_name": "John",
                "last_name": "Doe",
                "license_number": "invalid",  # wrong format
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_passwords_dont_match(self):
        form = DriverCreationForm(
            data={
                "username": "testdriver",
                "password1": "strong_pass_123",
                "password2": "different_pass",  # mismatch
                "license_number": "ABC12345",
            }
        )
        self.assertFalse(form.is_valid())


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="test1234",
            license_number="ABC12345",
        )

    def test_valid_car_form(self):
        form = CarForm(
            data={
                "model": "Camry",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.driver.id],
            }
        )
        self.assertTrue(form.is_valid())

    def test_car_form_without_drivers_is_valid(self):
        """drivers field is not required — car can exist with no assigned drivers"""
        form = CarForm(
            data={
                "model": "Camry",
                "manufacturer": self.manufacturer.id,
                "drivers": [],
            }
        )
        self.assertTrue(form.is_valid())

    def test_car_form_missing_model(self):
        form = CarForm(
            data={
                "model": "",
                "manufacturer": self.manufacturer.id,
                "drivers": [],
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)

    def test_car_form_missing_manufacturer(self):
        form = CarForm(
            data={
                "model": "Camry",
                "manufacturer": "",
                "drivers": [],
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("manufacturer", form.errors)


class SearchFormsTest(TestCase):
    def test_driver_search_form_valid(self):
        form = DriverSearchForm(data={"username": "john"})
        self.assertTrue(form.is_valid())

    def test_driver_search_form_empty_is_valid(self):
        """Empty search should be valid — returns all results"""
        form = DriverSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())

    def test_car_search_form_valid(self):
        form = CarSearchForm(data={"model": "Camry"})
        self.assertTrue(form.is_valid())

    def test_car_search_form_empty_is_valid(self):
        form = CarSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_valid(self):
        form = ManufacturerSearchForm(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_empty_is_valid(self):
        form = ManufacturerSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())
