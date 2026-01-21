from django.test import TestCase

from taxi.forms import DriverCreationForm


class TestDriverCreationForm(TestCase):
    def test_driver_license_number_validation(self):
        invalid_form_data = {
            "username": "TestUser1",
            "password1": "abcalpha",
            "password2": "abcalpha",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "license_number": "AB123456$",
        }
        valid_form_data = {
            "username": "TestUser2",
            "password1": "abcalpha",
            "password2": "abcalpha",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "license_number": "ABC12345",
        }

        invalid_form = DriverCreationForm(data=invalid_form_data)
        valid_form = DriverCreationForm(data=valid_form_data)

        self.assertFalse(invalid_form.is_valid())
        self.assertTrue(valid_form.is_valid())
