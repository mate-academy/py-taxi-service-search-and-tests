from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        ManufacturerSearchForm,
                        CarSearchForm, DriverSearchForm)


class FormsTest(TestCase):
    def test_driver_creation_form_with_is_valid(self):
        form_data = {
            "username": "valuc",
            "password1": "Test22021994",
            "password2": "Test22021994",
            "first_name": "Dmitriy",
            "last_name": "Dobkin",
            "license_number": "KLB12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form(self):
        form_data = {
            "name": "Test"
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        form_data = {
            "model": "Test"
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form(self):
        form_data = {
            "username": "Test",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
