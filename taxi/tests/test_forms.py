from django.test import TestCase

from taxi.forms import DriverCreationForm, validate_license_number


class FormsTest(TestCase):

    def test_driver_creation_with_license_number_first_name_last_name(self):
        form_data = {
            "username": "test_user",
            "first_name": "test_firstname",
            "last_name": "test_lastname",
            "password1": "pass1234",
            "password2": "pass1234",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_validation(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")
        self.assertRegex(validate_license_number("ABC12345"), "^[A-Z]{3}\d{5}$")
