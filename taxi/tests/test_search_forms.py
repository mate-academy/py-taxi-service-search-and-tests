from django.test import TestCase
from taxi.forms import DriverSearchForm, CarSearchForm, ManufacturerSearchForm


class SearchFormTests(TestCase):

    def test_driver_search_form_defaults_to_empty(self):
        ff = DriverSearchForm(data={})
        self.assertTrue(ff.is_valid())
        self.assertEqual(ff.cleaned_data["username"], "")

    def test_driver_search_form_accepts_username(self):
        ff = DriverSearchForm(data={"username": "alice"})
        self.assertTrue(ff.is_valid())
        self.assertEqual(ff.cleaned_data["username"], "alice")

    def test_car_search_form_defaults_to_empty(self):
        ff = CarSearchForm(data={})
        self.assertTrue(ff.is_valid())
        self.assertEqual(ff.cleaned_data["model"], "")

    def test_car_search_form_accepts_model(self):
        ff = CarSearchForm(data={"model": "Corolla"})
        self.assertTrue(ff.is_valid())
        self.assertEqual(ff.cleaned_data["model"], "Corolla")

    def test_manufacturer_search_form_defaults_to_empty(self):
        ff = ManufacturerSearchForm(data={})
        self.assertTrue(ff.is_valid())
        self.assertEqual(ff.cleaned_data["name"], "")

    def test_manufacturer_search_form_accepts_name(self):
        ff = ManufacturerSearchForm(data={"name": "Toyota"})
        self.assertTrue(ff.is_valid())
        self.assertEqual(ff.cleaned_data["name"], "Toyota")
