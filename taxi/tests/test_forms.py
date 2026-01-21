from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Car, Driver, Manufacturer


class CarFormTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="USA"
        )
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="password123",
            license_number="ABC12345"
        )

    def test_car_form_valid(self):
        form_data = {
            "model": "Tesla",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self):
        form_data = {
            "manufacturer": self.manufacturer.id,
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)


class DriverCreationFormTests(TestCase):
    def setUp(self):
        self.username = "newdriver"
        self.password = "valid_password_123"
        self.license_number = "ABC98765"

    def test_driver_creation_form_valid(self):
        form_data = {
            "username": self.username,
            "password1": self.password,
            "password2": self.password,
            "license_number": self.license_number,
            "first_name": "John",
            "last_name": "Doe"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_without_license_number(self):
        form_data = {
            "username": self.username,
            "password1": self.password,
            "password2": self.password,
            "first_name": "John",
            "last_name": "Doe"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="existingdriver",
            password="password123",
            license_number="XYZ12345"
        )

    def test_driver_license_update_form_valid(self):
        form_data = {
            "license_number": "NEW76543"
        }
        form = DriverLicenseUpdateForm(data=form_data, instance=self.driver)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid_license(self):
        form_data = {
            "license_number": "invalid"
        }
        form = DriverLicenseUpdateForm(data=form_data, instance=self.driver)
        self.assertFalse(form.is_valid())

    def test_driver_license_update_form_invalid_without_license_number(self):
        form_data = {}
        form = DriverLicenseUpdateForm(data=form_data, instance=self.driver)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverSearchFormTests(TestCase):
    def test_driver_search_form_valid(self):
        form_data = {
            "username": "testdriver"
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_empty(self):
        form_data = {}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class CarSearchFormTests(TestCase):
    def test_car_search_form_valid(self):
        form_data = {
            "model": "Tesla"
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form_empty(self):
        form_data = {}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTests(TestCase):
    def test_manufacturer_search_form_valid(self):
        form_data = {
            "name": "Test Manufacturer"
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_empty(self):
        form_data = {}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
