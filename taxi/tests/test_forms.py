from django.test import TestCase

from taxi.forms import (
    CarSearchForm,
    DriverCreationForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)


class CreateDriverFormTest(TestCase):
    def test_driver_create_with_licence_first_last_name_is_valid(self):
        form_data = {
            "username": "user123",
            "password1": "pa$$word123",
            "password2": "pa$$word123",
            "first_name": "John",
            "last_name": "Rider",
            "license_number": "ABC56984",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverSearchFormTest(TestCase):
    def test_search(self):
        form_data = {"username": "bmw"}
        form = DriverSearchForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class CarSearchFormTest(TestCase):
    def test_search(self):
        form_data = {"car_model": "bmw"}
        form = CarSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class ManufacturerSearchFormTest(TestCase):
    def test_search(self):
        form_data = {"name": "bmw"}
        form = ManufacturerSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

