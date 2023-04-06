from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_number_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "pass12345",
            "password2": "pass12345",
            "first_name": "Test First name",
            "last_name": "Test Last name",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_update_license_form_if_one_letter(self):
        form_data = {"license_number": "A12345"}
        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_update_license_form_if_four_digits(self):
        form_data = {"license_number": "ABC1234"}
        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_update_license_form_if_char_more_than_eight(self):
        form_data = {"license_number": "ABCD123456"}
        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
