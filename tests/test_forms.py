from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    ManufacturerNameSearchForm,
    DriverUsernameSearchForm,
    CarModelSearchForm
)


class FormTest(TestCase):
    def test_create_driver_license_number_first_and_last_name_is_valid(self):
        form_data = {
            "username": "admin",
            "first_name": "name",
            "last_name": "last",
            "license_number": "ASW12345",
            "password1": "admin12345",
            "password2": "admin12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_create_driver_with_incorrect_license_number_is_not_valid(self):
        form_data = {
            "username": "admin",
            "first_name": "name",
            "last_name": "last",
            "license_number": "not_valid",
            "password1": "admin12345",
            "password2": "admin12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_update_license_number_with_incorrect_data(self):
        form_data = {
            "license_number": "not_valid",
        }

        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())


class SearchFormTests(TestCase):

    def test_valid_form_manufacturer(self):
        form_data = {"name": "Example Manufacturer"}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_label_manufacturer(self):
        form = ManufacturerNameSearchForm()
        self.assertEqual(form.fields["name"].label, "")

    def test_form_widget_manufacturer(self):
        form = ManufacturerNameSearchForm()
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"], "Search..."
        )

    def test_valid_form_driver(self):
        form_data = {"username": "Example Driver"}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_label_driver(self):
        form = DriverUsernameSearchForm()
        self.assertEqual(form.fields["username"].label, "")

    def test_form_widget_driver(self):
        form = DriverUsernameSearchForm()
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"], "Search..."
        )

    def test_valid_form_car(self):
        form_data = {"model": "Example Model"}
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_label_car(self):
        form = CarModelSearchForm()
        self.assertEqual(form.fields["model"].label, "")

    def test_form_widget_car(self):
        form = CarModelSearchForm()
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"], "Search..."
        )
