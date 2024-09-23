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
            "license_number": "license number",
            "first_name": "test first name",
            "last_name": "test last name",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_car_search_form(self):
        form_data = {
            "model": "Audi"
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form(self):
        form_data = {
            "username": "paul.smith"
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form_data = {
            "name": "Audi AG"
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
