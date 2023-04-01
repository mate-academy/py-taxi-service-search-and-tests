from django.test import TestCase

from taxi.forms import DriverSearchForm, CarSearchForm, ManufacturerSearchForm


class DriverSearchFormTestCase(TestCase):
    def test_driver_search_form(self):
        form_data = {"name": "John"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "John")


class CarSearchFormTestCase(TestCase):
    def test_car_search_form(self):
        form_data = {"model": "Tesla"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Tesla")


class ManufacturerSearchFormTestCase(TestCase):
    def test_manufacturer_search_form(self):
        form_data = {"name": "Toyota"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Toyota")
