from django import forms
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    CarForm,
    CarSearchForm,
    ManufacturerSearchForm,
    DriverSearchForm
)


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_number_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "TEST",    # no valid license_number
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data["license_number"] = "AAA12345"  # valid license_number
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data, form_data)

    def test_drivers_widget(self):
        form = CarForm()
        self.assertIsInstance(
            form.fields["drivers"].widget,
            forms.CheckboxSelectMultiple
        )


class SearchFormTest(TestCase):
    def test_car_search_form(self):
        form_data = {"model": "Test"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {"model": ""}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        self.assertIsInstance(form.fields["model"].widget, forms.TextInput)
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            "Search by car's model..."
        )

        self.assertEqual(form.fields["model"].max_length, 255)

    def test_manufacturer_search_form(self):
        form_data = {"name": "Test"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {"name": ""}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        self.assertIsInstance(form.fields["name"].widget, forms.TextInput)
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Search by manufacturer's name..."
        )

        self.assertEqual(form.fields["name"].max_length, 255)

    def test_driver_search_form(self):
        form_data = {"username": "Test"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        self.assertIsInstance(form.fields["username"].widget, forms.TextInput)
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Search by username..."
        )

        self.assertEqual(form.fields["username"].max_length, 150)
