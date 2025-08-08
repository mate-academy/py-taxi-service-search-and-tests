from django.test import TestCase

from taxi.forms import DriverCreationForm


class TestForm(TestCase):
    def test_driver_creation_with_all_custom_params(self):
        form_data = {
            "username": "test_user",
            "password1": "<PASS1234WORD>",
            "password2": "<PASS1234WORD>",
            "last_name": "test_last_name",
            "first_name": "test_first_name",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)

        print(form.errors)
        self.assertTrue(form.is_valid())

        self.assertEqual(
            form.cleaned_data["username"],
            form_data["username"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"]
        )
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )
