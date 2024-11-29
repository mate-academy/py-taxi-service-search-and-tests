from django.test import TestCase
from taxi.forms import DriverSearchForm, CarSearchForm, ManufacturerSearchForm


class DriverSearchFormTest(TestCase):
    def test_valid_data(self):
        form = DriverSearchForm(data={"username": "Ivan"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "Ivan")

    def test_empty_data(self):
        form = DriverSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")


class CarSearchFormTest(TestCase):
    def test_valid_data(self):
        form = CarSearchForm(data={"model": "Civic"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Civic")

    def test_empty_data(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")


class ManufacturerSearchFormTest(TestCase):
    def test_valid_data(self):
        form = ManufacturerSearchForm(data={"name": "Tesla"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Tesla")

    def test_empty_data(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")
