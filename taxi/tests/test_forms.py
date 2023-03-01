from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm
)
from taxi.models import Car, Manufacturer


class FormsTests(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "my987test",
            "password2": "my987test",
            "first_name": "First_test",
            "last_name": "Last_test",
            "license_number": "TES12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class TestSearchForm(TestCase):
    def test_manufacturer(self):
        form_data = {
            "name": "Test name",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car(self):
        form_data = {
            "model": "Test model",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver(self):
        form_data = {
            "username": "test_user",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
