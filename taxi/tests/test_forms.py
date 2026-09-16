from django.test import TestCase

from taxi.forms import DriverSearchForm, CarSearchForm, ManufacturerSearchForm


class DriverSearchFormTests(TestCase):
    def test_driver_search_form_valid(self):
        form_data = {"username": "user"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])

    def test_driver_search_form_valid_empty(self):
        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")


class CarSearchFormTests(TestCase):
    def test_car_search_form_valid(self):
        form_data = {"model": "model"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], form_data["model"])

    def test_car_search_form_valid_empty(self):
        form_data = {"model": ""}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")


class ManufacturerSearchFormTests(TestCase):
    def test_manufacturer_search_form_valid(self):
        form_data = {"name": "name"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], form_data["name"])

    def test_manufacturer_search_form_valid_empty(self):
        form_data = {"name": ""}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")
