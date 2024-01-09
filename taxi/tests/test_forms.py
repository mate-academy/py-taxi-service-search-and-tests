from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_number_first_name_last_name(
            self
    ):
        form_data = {
            "username": "test",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "WAR12345"
        }
        form = DriverCreationForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverSearchFormTest(TestCase):
    def test_valid_search_form(self):
        form_data = {
            "username": "test_username",
        }
        form = DriverSearchForm(data=form_data)

        self.assertTrue(form.is_valid())


class CarCreationFormTest(TestCase):
    def test_empty_search_form(self):
        form_data = {}
        form = DriverSearchForm(data=form_data)

        self.assertTrue(form.is_valid())


class ManufacturerCreationFormTest(TestCase):
    def test_invalid_search_form(self):
        form_data = {
            "name": "testtest",
        }

        form = ManufacturerSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
