from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm
)


class FormTests(TestCase):

    def test_driver_creation_form_invalid(self):
        form_data = {
            "license_number": "test_license_number",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_car_search_form(self):
        form_data = {
            "model": "test_model"
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form(self):
        form_data = {
            "username": "test_username",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form_data = {
            "name": "test_model"
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
