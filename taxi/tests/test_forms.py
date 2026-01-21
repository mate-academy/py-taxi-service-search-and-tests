from django.test import TestCase

from django import forms
from taxi.forms import (
    DriverLicenseUpdateForm,
    DriverCreationForm,
    CarForm,
    DriverUsernameSearchForm,
    CarModelSearchForm,
    ManufacturerNameSearchForm,
)


class FormTests(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "2wsxvfr4",
            "password2": "2wsxvfr4",
            "first_name": "Test",
            "last_name": "Test",
            "license_number": "TST12345",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_is_valid(self):
        form_data = {"license_number": "QWE98765"}

        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_check_license_number_has_eight_chars(self):
        form = DriverLicenseUpdateForm(data={"license_number": "12345"})
        self.assertFalse(form.is_valid())

    def test_first_three_chars_are_letters(self):
        form = DriverLicenseUpdateForm(data={"license_number": "TO512345"})
        self.assertFalse(form.is_valid())

    def test_last_five_chars_are_digits(self):
        form = DriverLicenseUpdateForm(data={"license_number": "TOMA2345"})
        self.assertFalse(form.is_valid())

    def test_valid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ASD12345"})
        self.assertTrue(form.is_valid())

    def test_driver_update_license_form_is_not_valid(self):
        form_data = {"license_number": "123456qwe"}

        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_car_form_field_widget(self):
        form = CarForm()
        self.assertIsInstance(
            form.fields["drivers"].widget, forms.CheckboxSelectMultiple
        )

    def test_driver_search_form_field_widget(self):
        form = DriverUsernameSearchForm()
        print(
            "form.fields['username']: ",
            form.fields["username"].widget.attrs["placeholder"],
        )
        self.assertIsInstance(form.fields["username"].widget, forms.TextInput)
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Search by username"
        )

    def test_car_search_form_field_widget(self):
        form = CarModelSearchForm()

        self.assertIsInstance(form.fields["model"].widget, forms.TextInput)
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"], "Search by model"
        )

    def test_manufacturer_search_form_field_widget(self):
        form = ManufacturerNameSearchForm()

        self.assertIsInstance(form.fields["name"].widget, forms.TextInput)
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"], "Search by name"
        )
