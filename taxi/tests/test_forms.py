from django.test import TestCase
from django import forms

from taxi.forms import (
    DriverCreationForm,
    DriverUsernameSearchForm,
    CarModelSearchForm,
    ManufacturerNameSearchForm
)


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "test name",
            "last_name": "test last",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_form_widget(self):
        form = DriverUsernameSearchForm()

        self.assertIsInstance(form.fields["username"].widget, forms.TextInput)

    def test_manufacturer_search_form_widget(self):
        form = ManufacturerNameSearchForm()

        self.assertIsInstance(form.fields["name"].widget, forms.TextInput)

    def test_car_search_form_widget(self):
        form = CarModelSearchForm()

        self.assertIsInstance(form.fields["model"].widget, forms.TextInput)
