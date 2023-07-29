from django.test import TestCase

from taxi.forms import DriverSearchForm, CarSearchForm, ManufacturerSearchForm


class FormsTests(TestCase):
    def test_driver_search_form_is_valid(self):
        form_data = {
            "username": "new_user"
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_search_form_is_valid(self):
        form_data = {
            "model": "new_model"
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form_is_valid(self):
        form_data = {
            "name": "new_manufacturer"
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
