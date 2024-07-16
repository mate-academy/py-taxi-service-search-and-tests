from django.test import TestCase

from taxi.forms import (
    DriverUsernameSearchForm,
    CarModelSearchForm,
    ManufacturerNameSearchForm
)


class SearchFormTest(TestCase):
    def test_driver_username_search_form(self):
        form_data = {
            "username": "test"
        }
        form = DriverUsernameSearchForm(
            data=form_data
        )
        self.assertTrue(form.is_valid())

    def test_car_model_search_form(self):
        form_data = {
            "model": "X5"
        }
        form = CarModelSearchForm(
            data=form_data
        )
        self.assertTrue(form.is_valid())

    def test_manufacturer_name_search_form(self):
        form_data = {
            "name": "BMW"
        }
        form = ManufacturerNameSearchForm(
            data=form_data
        )
        self.assertTrue(form.is_valid())
