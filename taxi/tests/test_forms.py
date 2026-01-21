from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)
from taxi.models import (
    Car,
    Driver,
    Manufacturer
)


class DriverCreationFormTests(TestCase):

    def setUp(self):
        self.valid_form_data = {
            "username": "user",
            "password1": "userpass123",
            "password2": "userpass123",
            "first_name": "Michael",
            "last_name": "Schumacher",
            "license_number": "MSA12345"
        }

    def get_form(self, **kwargs):
        form_data = self.valid_form_data.copy()
        form_data.update(kwargs)
        return DriverCreationForm(data=form_data)

    def test_clean_license_number_valid(self):
        form = self.get_form(license_number="ABC12345")
        self.assertTrue(form.is_valid())

    def test_clean_license_number_invalid(self):
        form = self.get_form(license_number="Abc12345")
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form(self):
        form = DriverCreationForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.valid_form_data)


class SearchFormsTests(TestCase):

    def test_driver_search_form_valid(self):
        form_data = {"username": "Michael"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "Michael")

    def test_driver_search_form_empty(self):
        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_car_search_form_valid(self):
        form_data = {"model": "Touareg"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Touareg")

    def test_car_search_form_empty(self):
        form_data = {"model": ""}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_manufacturer_search_form_valid(self):
        form_data = {"name": "Volkswagen"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Volkswagen")

    def test_manufacturer_search_form_empty(self):
        form_data = {"name": ""}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")
