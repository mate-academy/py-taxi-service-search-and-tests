from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Driver, Manufacturer, Car


class SearchFormTest(TestCase):
    def test_manufacturer_search(self):
        form = ManufacturerSearchForm(data={"name": "BMW"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "BMW")

    def test_manufacturer_search_empty(self):
        form = ManufacturerSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_manufacturer_search_no_data(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_driver_search(self):
        form = DriverSearchForm(data={"username": "test1"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test1")

    def test_driver_search_empty(self):
        form = DriverSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_driver_search_no_data(self):
        form = DriverSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_car_search(self):
        form = CarSearchForm(data={"model": "X5"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "X5")

    def test_car_search_empty(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_car_search_no_data(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")
