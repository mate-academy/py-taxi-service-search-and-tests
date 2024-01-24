from unittest import TestCase

from taxi.forms import DriverCreationForm, DriverSearchForm, CarSearchForm, ManufacturerSearchForm


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "test_username",
            "password1": "testpass123456",
            "password2": "testpass123456",
            "license_number": "AAA11111",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)


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
