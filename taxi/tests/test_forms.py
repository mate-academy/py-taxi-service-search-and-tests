from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):

    def setUp(self):
        self.form_data = {
            "username": "new_user",
            "password1": "pass12345",
            "password2": "pass12345",
            "first_name": "Test First name",
            "last_name": "Test Last name",
            "license_number": "ABC12345",
        }

    def test_driver_creation_form_with_license_number_is_valid(self):

        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_creation_form_with_license_number_is_invalid(self):
        license_numbers_test_cases = [
            "abc12345",
            "12345678",
            "ABC1234",
            "ABCD1234",
            "ABC12345678",
            "ABC1234!",
            " "
        ]
        for license_number in license_numbers_test_cases:
            self.form_data["license_number"] = license_number
            form = DriverCreationForm(data=self.form_data)
            self.assertFalse(form.is_valid())
