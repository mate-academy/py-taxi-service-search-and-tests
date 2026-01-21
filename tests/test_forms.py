from django.test import TestCase
from taxi.forms import (DriverCreationForm,
                        CarSearchForm,
                        ManufacturerSearchForm)


class TaxiFormsTest(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "testuser",
            "password1": "strongpassword",
            "password2": "strongpassword",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form_valid(self):
        form_data = {
            "model": "Corolla"
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_valid(self):
        form_data = {
            "name": "Toyota"
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
