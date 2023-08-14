from django.test import TestCase

from parameterized import parameterized
from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def setUp(self):
        self.valid_form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test second",
            "license_number": "ABC12345"
        }

    def test_driver_creation_form_with_license_number_is_valid(self):
        form = DriverCreationForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.valid_form_data)

    @parameterized.expand([
        ("ABC12",),
        ("12345678",),
        ("abc12345",),
        ("ABCccccc",),
    ])
    def test_invalid_license_number_formats(self, invalid_license_number):
        form_data = self.valid_form_data.copy()
        form_data["license_number"] = invalid_license_number
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
