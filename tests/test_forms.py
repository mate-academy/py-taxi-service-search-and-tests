from django.test import TestCase

from taxi.forms import DriverCreationForm, ManufacturerSearchForm, CarSearchForm, DriverSearchForm
from taxi.models import Manufacturer


class FormsTests(TestCase):
    def test_driver_create(self):
        data = {
            "username": "test1",
            "password1": "test234567",
            "password2": "test234567",
            "license_number": "AAA12345",
            "first_name": "test3",
            "last_name": "test4",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)


class ManufacturerSearchFormTest(TestCase):
    def test_search_by_name(self):
        form_data = {"name": "Honda"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Honda")


class CarSearchFormTest(TestCase):
    def test_search_by_model(self):
        form_data = {"model": "Accord"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Accord")


class DriverSearchFormTest(TestCase):
    def test_search_by_username(self):
        form_data = {"username": "test"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test")
