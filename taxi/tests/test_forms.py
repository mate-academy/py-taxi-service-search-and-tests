from django.test import TestCase
from taxi.forms import (
    DriverCreationForm,
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm
)


class FormsTests(TestCase):

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
            "model": "Toyota"
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form(self):
        form_data = {
            "username": "joyce.byers"
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form_data = {
            "name": "BMW"
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
