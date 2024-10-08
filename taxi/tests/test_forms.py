from django import forms
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm,
)


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "testdriver",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "Driver",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseUpdateFormTests(TestCase):
    def test_driver_license_update_form_valid(self):
        form_data = {
            "license_number": "ABC12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid_length(self):
        form_data = {
            "license_number": "1234567"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_invalid_format(self):
        form_data = {
            "license_number": "abc12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

        form_data = {
            "license_number": "ABC12A45"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverSearchFormTests(TestCase):
    def test_driver_search_form_valid(self):
        form = DriverSearchForm(data={"username": "testuser"})
        self.assertTrue(form.is_valid())

    def test_driver_search_form_empty(self):
        form = DriverSearchForm(data={})
        self.assertTrue(form.is_valid())


class CarSearchFormTests(TestCase):
    def test_car_search_form_valid(self):
        form = CarSearchForm(data={"model": "Test Model"})
        self.assertTrue(form.is_valid())

    def test_car_search_form_empty(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTests(TestCase):
    def test_manufacturer_search_form_valid(self):
        form = ManufacturerSearchForm(data={"name": "Test Manufacturer"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_empty(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())
