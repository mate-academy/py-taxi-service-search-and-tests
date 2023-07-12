from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm
)


class DriverFormTest(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "test_password_12345",
            "password2": "test_password_12345",
            "first_name": "Test name",
            "last_name": "Test last name",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)

    def test_validation_license_number(self):
        form_data = {
            "username": "test_user",
            "password1": "test_password_12345",
            "password2": "test_password_12345",
            "first_name": "Test name",
            "last_name": "Test last name",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["license_number"], "ABC12345")
        self.assertEqual(len(form.cleaned_data["license_number"]), 8)
        self.assertTrue(form.cleaned_data["license_number"][:3].upper())
        self.assertTrue(form.cleaned_data["license_number"][:3].isalpha())
        self.assertTrue(form.cleaned_data["license_number"][3:].isdigit())


class TestSearchForm(TestCase):
    def test_manufacturer_search_form(self):
        test_data = {"name": "Mazda"}
        form = ManufacturerSearchForm(data=test_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        test_data = {"model": "RX8"}
        form = CarSearchForm(data=test_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form(self):
        test_data = {"username": "Shuma"}
        form = DriverSearchForm(data=test_data)
        self.assertTrue(form.is_valid())
