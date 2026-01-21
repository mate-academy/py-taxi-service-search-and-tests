from django.test import TestCase
from taxi.forms import (
    DriverCreationForm,
    DriverUsernameSearchForm,
)


class DriverCreationFormTest(TestCase):
    def test_driver_creation_from_is_valid(self):
        form_data = {
            "username": "test",
            "password1": "test12345",
            "password2": "test12345",
            "license_number": "XYZ12345",
            "first_name": "Test first",
            "last_name": "Test last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class SearchFormTest(TestCase):
    def test_driver_username_search_form_is_valid(self):
        form_data = {"username": "test"}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
