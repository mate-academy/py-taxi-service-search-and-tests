from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm
)


class FormTest(TestCase):
    def test_driver_creation_form_with_license_etc_is_valid(self):
        form_data = {
            "username": "test1",
            "password1": "test123456",
            "password2": "test123456",
            "license_number": "TES12345",
            "first_name": "first_name",
            "last_name": "last_name",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_fields(self):
        form = DriverLicenseUpdateForm()
        expected_fields = ["license_number"]
        self.assertEqual(list(form.fields), expected_fields)

    def test_license_valid_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "TES12345"})
        self.assertTrue(form.is_valid())

    def test_license_number_invalid_letters(self):
        form = DriverLicenseUpdateForm(data={"license_number": "tes12345"})
        self.assertFalse(form.is_valid())

    def test_license_number_invalid_len(self):
        form = DriverLicenseUpdateForm(data={"license_number": "TES123456"})
        self.assertFalse(form.is_valid())
