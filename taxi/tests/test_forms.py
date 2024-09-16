from django.contrib.auth import get_user_model
from django import forms
from django.test import TestCase
from taxi.forms import (
    CarForm,
    DriverLicenseUpdateForm,
    CarSearchForm,
    ManufacturerSearchForm,
    DriversSearchForm,
)


class TestCarForm(TestCase):
    def test_drivers_field(self):
        form = CarForm()
        self.assertIsInstance(
            form.fields["drivers"], forms.ModelMultipleChoiceField
        )

        queryset = form.fields["drivers"].queryset
        self.assertEqual(queryset.model, get_user_model())


class TestDriverLicenseUpdateForm(TestCase):
    def test_driver_license_update_form_valid(self):
        data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        data = {
            "license_number": "ABCD",  # Invalid license number
        }
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())


class TestSearchFormValid(TestCase):
    def setUp(self):
        self.data = {
            "model": "Test Model",
        }

    def test_car_search_form_valid(self):
        form = CarSearchForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_valid(self):
        form = ManufacturerSearchForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_drivers_search_form_valid(self):
        form = DriversSearchForm(data=self.data)
        self.assertTrue(form.is_valid())
