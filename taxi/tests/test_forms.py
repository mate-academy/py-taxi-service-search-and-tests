from django.test import TestCase
from taxi.forms import (DriversSearchForm,
                        CarsSearchForm,
                        ManufacturersSearchForm)
from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name_is_valid(
            self
    ) -> None:
        form_data = {
            "username": "new_user",
            "password1": "test123user",
            "password2": "test123user",
            "license_number": "NUM12345",
            "first_name": "Test First",
            "last_name": "Test Last"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class SearchFormsTest(TestCase):

    def test_drivers_search_form_valid(self):
        form_data = {"username": "test_user"}
        form = DriversSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test_user")

    def test_drivers_search_form_empty(self):
        form_data = {"username": ""}
        form = DriversSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_cars_search_form_valid(self):
        form_data = {"model": "test_model"}
        form = CarsSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "test_model")

    def test_cars_search_form_empty(self):
        form_data = {"model": ""}
        form = CarsSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_manufacturers_search_form_valid(self):
        form_data = {"name": "test_name"}
        form = ManufacturersSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "test_name")

    def test_manufacturers_search_form_empty(self):
        form_data = {"name": ""}
        form = ManufacturersSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")
