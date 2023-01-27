from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm
)


class FormTest(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name(self):
        form_data = {
            "username": "new_driver",
            "password1": "user123test",
            "password2": "user123test",
            "license_number": "ABC12345",
            "first_name": "User",
            "last_name": "Shift",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_search_form_with_model(self):
        form_data = {
            "model": "Ford"
        }
        form = CarSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_form_with_username(self):
        form_data = {
            "username": "Driver777"
        }
        form = DriverSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form_with_name(self):
        form_data = {
            "name": "ZAZ"
        }
        form = ManufacturerSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
