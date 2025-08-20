from django.test import TestCase
from taxi.forms import (
    CarModelSearchForm,
    DriverUsernameSearchForm,
    ManufacturerNameSearchForm
)


class CarModelSearchFormTest(TestCase):
    def test_valid_form(self):
        form = CarModelSearchForm(data={"model": "Toyota"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Toyota")

    def test_valid_empty_form(self):
        form = CarModelSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_too_long_input(self):
        long_input = "-" * 52
        form = CarModelSearchForm(data={"model": long_input})
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)


class DriverUsernameSearchFormTest(TestCase):
    def test_valid_form(self):
        form = DriverUsernameSearchForm(data={"username": "John"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "John")

    def test_valid_empty_form(self):
        form = DriverUsernameSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_too_long_input(self):
        long_input = "-" * 52
        form = DriverUsernameSearchForm(data={"username": long_input})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class ManufacturerNameSearchFormTest(TestCase):
    def test_valid_form(self):
        form = ManufacturerNameSearchForm(data={"name": "KTM"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "KTM")

    def test_valid_empty_form(self):
        form = ManufacturerNameSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_too_long_input(self):
        long_input = "-" * 52
        form = ManufacturerNameSearchForm(data={"name": long_input})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
