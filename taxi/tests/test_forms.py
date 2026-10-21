from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverCreationFormTest(TestCase):
    def test_form_has_custom_fields(self):
        form = DriverCreationForm()

        self.assertIn("license_number", form.fields)
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)

    def test_invalid_license_number(self):
        form = DriverCreationForm(data={
            "username": "test_user",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
            "license_number": "abc12345",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_valid_license_number(self):
        form = DriverCreationForm(data={
            "username": "test_user",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
            "license_number": "ABC12345",
        })

        self.assertTrue(form.is_valid())
