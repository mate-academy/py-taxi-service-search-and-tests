from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm, DriverCreationForm


class DriverLicenseUpdateFormTests(TestCase):
    def test_invalid_length_license_number(self):
        form_data = {
            "license_number": "1"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_upper_characters_license_number(self):
        form_data = {
            "license_number": "aaa12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_digits_license_number(self):
        form_data = {
            "license_number": "AAA12t45"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_license_number(self):
        form_data = {
            "license_number": "AAA12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)


class DriverCreationFormTest(TestCase):
    def test_valid_data(self):
        form_data = {
            "username": "user",
            "password1": "test_pas123!",
            "password2": "test_pas123!",
            "first_name": "test_fn",
            "last_name": "test_ln",
            "license_number": "AAA12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
