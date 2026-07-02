from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_validate_license_number_form(self):
        user = {
            "first_name": "test",
            "last_name": "test",
            "username": "test",
            "email": "test@test.tes",
            "password1": "Test123Ww",
            "password2": "Test123Ww",
            "license_number": "TES12345",
        }
        form = DriverCreationForm(data=user)
        self.assertTrue(form.is_valid(), msg=form.errors)
        self.assertEqual(
            form.cleaned_data["license_number"],
            user["license_number"])
