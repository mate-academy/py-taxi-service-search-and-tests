from django.test import TestCase
from taxi.forms import DriverCreationForm


class DriverCreationFormTests(TestCase):
    def test_valid_form(self):
        data = {
            "username": "test_user",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "ABC13112",
            "first_name": "Test",
            "last_name": "User",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid(), form.errors.as_text())
        self.assertEqual(form.cleaned_data["username"], data["username"])
        self.assertEqual(form.cleaned_data["license_number"],
                         data["license_number"])
        self.assertEqual(form.cleaned_data["first_name"], data["first_name"])
        self.assertEqual(form.cleaned_data["last_name"], data["last_name"])
