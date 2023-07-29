from django.test import TestCase

from taxi.forms import (
    DriverUsernameSearchForm,
    CarModelSearchForm,
    ManufacturerNameSearchForm
)


class FormsTests(TestCase):
    def test_driver_search_form_is_valid(self):
        form_data = {
            "username": "new_user"
        }
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_search_form_is_valid(self):
        form_data = {
            "model": "new_model"
        }
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form_is_valid(self):
        form_data = {
            "name": "new_manufacturer"
        }
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
