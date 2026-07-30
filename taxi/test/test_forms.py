from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverFormTests(TestCase):

    def setUp(self):
        self.valid_data = {
            "username": "john",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "ABC12345",
        }

    def test_valid_license_number(self):
        form = DriverCreationForm(
            data=self.valid_data
        )

        self.assertTrue(form.is_valid())

    def test_license_number_wrong_length(self):
        data = self.valid_data.copy()
        data["license_number"] = "ABC123"

        form = DriverCreationForm(data=data)

        self.assertFalse(form.is_valid())

    def test_license_number_wrong_letters(self):
        data = self.valid_data.copy()
        data["license_number"] = "abc12345"

        form = DriverCreationForm(data=data)

        self.assertFalse(form.is_valid())
