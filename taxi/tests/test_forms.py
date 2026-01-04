from django.test import TestCase
from taxi.forms import CarSearchForm, DriverSearchForm, ManufacturerSearchForm


class SearchFormTests(TestCase):
    def test_driver_username_search(self):
        form_data = {
            "username": "test"
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_name_search(self):
        form_data = {
            "name": "test"
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_model_search(self):
        form_data = {
            "model": "test"
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
