from django.core.exceptions import ValidationError
from django.test import TestCase
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    validate_license_number
)

from taxi.models import Car, Driver, Manufacturer


class FormsTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="BingChilling",
            country="China"
        )
        self.car = Car.objects.create(
            model="test_model_car",
            manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create(
            username="riceman",
            password="ChinaIsTheBest",
            first_name="BimBim",
            last_name="BamBam",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)

    def test_car_form_valid(self) -> None:
        form_data = {
            "model": "test_model3434",
            "manufacturer": self.manufacturer,
            "drivers": [self.driver]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self) -> None:
        data = {
            "model": "",
        }
        form = CarForm(data=data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_valid(self) -> None:
        data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "first_name": "Test",
            "last_name": "User",
            "license_number": "ABC12349",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid(self) -> None:
        data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword456",
            "license_number": "AB12",
            "first_name": "Test",
            "last_name": "User",
        }
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_driver_license_update_form_valid(self) -> None:
        data = {
            "license_number": "ABC12545",
        }
        form = DriverLicenseUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self) -> None:
        data = {
            "license_number": "AB12",
        }
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_car_search_form_valid(self) -> None:
        data = {
            "query": "Test Model",
        }
        form = CarSearchForm(data=data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_valid(self) -> None:
        data = {
            "query": "testuser",
        }
        form = DriverSearchForm(data=data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_valid(self) -> None:
        data = {
            "query": "Test Manufacturer",
        }
        form = ManufacturerSearchForm(data=data)
        self.assertTrue(form.is_valid())

    def test_short_license_number(self):
        with self.assertRaisesMessage(ValidationError, "License number should consist of 8 characters"):
            validate_license_number("ABC123")

    def test_long_license_number(self):
        with self.assertRaisesMessage(ValidationError, "License number should consist of 8 characters"):
            validate_license_number("ABC1234567")

    def test_lowercase_initial_characters(self):
        with self.assertRaisesMessage(ValidationError, "First 3 characters should be uppercase letters"):
            validate_license_number("abc12345")

    def test_non_letter_initial_characters(self):
        with self.assertRaisesMessage(ValidationError, "First 3 characters should be uppercase letters"):
            validate_license_number("12312345")

    def test_non_digit_trailing_characters(self):
        with self.assertRaisesMessage(ValidationError, "Last 5 characters should be digits"):
            validate_license_number("ABC12XYZ")