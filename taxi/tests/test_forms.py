from django import forms
from django.test import TestCase
from taxi.forms import (
    DriverCreationForm,
    CarSearchForm,
    ManufacturerSearchForm,
    DriverSearchForm
)


class FormTest(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "test123test",
            "password2": "test123test",
            "first_name": "Test first",
            "last_name": "Last test",
            "license_number": "FGD45678"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form(self):
        form = DriverSearchForm()
        self.assertIsInstance(form.fields["username"].widget, forms.TextInput)

    def test_car_search_form(self):
        form = CarSearchForm()
        self.assertIsInstance(form.fields["model"].widget, forms.TextInput)

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm()
        self.assertIsInstance(form.fields["name"].widget, forms.TextInput)
