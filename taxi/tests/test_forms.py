from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    CarForm,
    validate_license_number,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Manufacturer


class CarFormTest(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="Test Country"
        )
        driver = get_user_model().objects.create(
            username="test_driver",
            password="test1234"
        )
        self.form_data = {
            "model": "TestForm Model",
            "manufacturer": manufacturer.id,
            "drivers": [driver.id],
        }

    def test_car_form_valid(self):
        form = CarForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_cleaned_data(self):
        form = CarForm(data=self.form_data)
        form.is_valid()
        self.assertEqual(
            form.cleaned_data["model"],
            self.form_data["model"]
        )
        self.assertEqual(
            form.cleaned_data["manufacturer"].id,
            self.form_data["manufacturer"]
        )
        drivers_queryset = get_user_model().objects.filter(
            id=self.form_data["drivers"][0]
        )
        self.assertQuerysetEqual(
            form.cleaned_data["drivers"],
            drivers_queryset
        )

    def test_car_form_drivers_field(self):
        form = CarForm(data=self.form_data)
        self.assertIn("drivers", form.fields)
        self.assertIsInstance(
            form.fields["drivers"].widget,
            forms.CheckboxSelectMultiple
        )

    def test_car_form_drivers_queryset(self):
        form = CarForm(data=self.form_data)
        self.assertEqual(
            form.fields["drivers"].queryset.count(),
            get_user_model().objects.count(),
        )


class DriverFormTest(TestCase):
    def test_license_number_validation(self):
        valid_license_number = "ABC12345"
        self.assertEqual(
            validate_license_number(valid_license_number),
            valid_license_number
        )

        invalid_license_numbers = [
            ("ABC1234", "License number should consist of 8 characters"),
            ("abc12345", "First 3 characters should be uppercase letters"),
            ("12345678", "First 3 characters should be uppercase letters"),
            ("ABCD2345", "Last 5 characters should be digits")
        ]
        for license_number, expected_error in invalid_license_numbers:
            with self.assertRaises(ValidationError) as context:
                validate_license_number(license_number)
            self.assertIn(expected_error, str(context.exception))


class DriverSearchFormTest(TestCase):
    def test_driver_form_valid_data(self):
        form_data = {
            "username": "test_driver",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_form_invalid_data(self):
        form_data = {
            "username": "a" * 101,
        }
        form = DriverSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_form_empty_username(self):
        form_data = {
            "username": "",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class CarSearchFormTest(TestCase):

    def test_car_form_valid_data(self):
        form_data = {
            "model": "Test Model",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid_data(self):
        form_data = {
            "model": "a" * 101,
        }
        form = CarSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_car_form_empty_model(self):
        form_data = {
            "model": "",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTest(TestCase):

    def test_manufacturer_form_valid_data(self):
        form_data = {
            "name": "Test Manufacturer",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_form_invalid_data(self):
        form_data = {
            "name": "a" * 101,
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_manufacturer_form_empty_name(self):
        form_data = {
            "name": "",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
