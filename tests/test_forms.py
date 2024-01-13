from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)


class FormsTests(TestCase):
    def test_driver_creation_form_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "MAR12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverSearchFormTest(TestCase):
    def test_driver_search_form_is_valid(self):
        form_data = {
            "username": "test_username",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class CarSearchFormTest(TestCase):
    def test_car_search_form_is_valid(self):
        form_data = {
            "model": "test_model",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_form_is_valid(self):
        form_data = {
            "name": "test_name",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
