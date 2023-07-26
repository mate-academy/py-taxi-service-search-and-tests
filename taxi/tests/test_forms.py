from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "testuser",
            "license_number": "ABC12345",
            "first_name": "fime",
            "last_name": "lame",
            "password1": "test12345",
            "password2": "test12345",
        }

    def test_driver_creation_form_with_license_first_last_name(self):

        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, self.form_data)

    def test_driver_licence_validation(self):
        licence_to_long = DriverCreationForm(
            data={"licence_number": "ABC1234567"}
        )
        self.assertFalse(licence_to_long.is_valid())

        licence_contains_digit = DriverCreationForm(
            data={"licence_number": "ABC12ABC"}
        )
        self.assertFalse(licence_contains_digit.is_valid())

        licence_first_letter = DriverCreationForm(
            data={"licence_number": "1BC12345"}
        )
        self.assertFalse(licence_first_letter.is_valid())
