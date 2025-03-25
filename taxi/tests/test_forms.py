from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    CarSearchForm,
    CarForm
)
from taxi.models import Manufacturer


class CarFormsTests(TestCase):
    def test_car_form_is_valid(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        driver = get_user_model().objects.create_user(
            username="test1",
            password="test123",
            first_name="first",
            last_name="last",
            license_number="ABC12345",
        )
        form_data = {
            "model": "Test",
            "manufacturer": manufacturer.id,
            "drivers": [driver.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], form_data["model"])
        self.assertEqual(
            form.cleaned_data["manufacturer"].id,
            form_data["manufacturer"]
        )
        self.assertEqual(
            [driver.id for driver in form.cleaned_data["drivers"]],
            form_data["drivers"]
        )

    def test_car_form_drivers_is_checkbox_select_multiple(self):
        form = CarForm()
        self.assertIsInstance(
            form.fields["drivers"].widget,
            forms.CheckboxSelectMultiple
        )

    def test_car_search_form_with_valid_data(self):
        form_data = {
            "model": "Test"
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form_without_data(self):
        form_data = {
            "model": ""
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form_with_too_long_model(self):
        form_data = {
            "model": 256 * "n"
        }
        form = CarSearchForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverFormsTests(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form(self):
        license_data = {
            "license_number": "CBA54321"
        }
        form = DriverLicenseUpdateForm(data=license_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"],
            license_data["license_number"]
        )

    def test_driver_search_form_with_valid_data(self):
        form_data = {
            "username": "new_user"
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_without_data(self):
        form_data = {
            "username": ""
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_with_too_long_username(self):
        form_data = {
            "username": 256 * "n"
        }
        form = DriverSearchForm(data=form_data)
        self.assertFalse(form.is_valid())


class ManufacturerFormsTests(TestCase):
    def test_manufacturer_search_form_with_valid_data(self):
        form_data = {
            "name": "Test"
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_without_data(self):
        form_data = {
            "name": ""
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_with_too_long_name(self):
        form_data = {
            "name": 256 * "n"
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
