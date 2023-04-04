from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverSearchForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_is_valid(self):
        form_data = {
            "username": "Marichka",
            "password1": "z54bvFG543",
            "password2": "z54bvFG543",
            "first_name": "Maria",
            "last_name": "Clinton",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_with_license_number_is_invalid(self):
        invalid_license_numbers = [
            "INVALID_LICENSE_NUMBER",
            "123456789",
            "123456789012345678901",
            "A12B!#C4D",
            "AB-1234-CD",
            "",
        ]

        for license_number in invalid_license_numbers:
            form_data = {
                "username": "user",
                "password1": "user12345",
                "password2": "user12345",
                "first_name": "user_name",
                "last_name": "user_last_name",
                "license_number": license_number,
            }
            form = DriverCreationForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertIn("license_number", form.errors)
