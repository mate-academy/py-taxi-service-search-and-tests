from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Driver


class FormsTests(TestCase):

    def test_driver_creation_form_license_number_first_name_last_name(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test",
            "last_name": "last",
            "license_number": "QWE12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

        self.assertDictEqual(form.cleaned_data, form_data)

    def test_driver_form_update_incorrect_first_character(self):
        form_data = {"license_number": "qWE12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_form_update_incorrect_len(self):
        form_data = {"license_number": "QWE123456"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_form_update_incorrect_last_digits(self):
        form_data = {"license_number": "QWE1234SS"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
