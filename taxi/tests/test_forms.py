from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm,
)


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "user",
            "password1": "Password_123",
            "password2": "Password_123",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "TES45678",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form(self):
        form_data = {"name": "test"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        form_data = {"model": "test"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form(self):
        form_data = {"username": "user"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
