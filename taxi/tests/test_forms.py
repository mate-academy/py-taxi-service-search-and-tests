from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)


class FormsTests(TestCase):
    def test_drivers_creation_form(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_drivers_search_form(self):
        form_data = {
            "username": "new_user",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_search_form(self):
        form_data = {
            "model": "new_model",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form(self):
        form_data = {
            "name": "new_name",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
