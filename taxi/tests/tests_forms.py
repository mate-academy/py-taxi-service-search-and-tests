from django.test import TestCase

from taxi.forms import DriverCreationForm, validate_license_number


class FormsTests(TestCase):
    def test_driver_creation(self):
        form_data = {
            "username": "driver",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "user12test",
            "password2": "user12test",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_validate_license_number(self):
        self.assertEqual(len(validate_license_number("ABC12345")), 8)
        self.assertTrue(validate_license_number("ABC12345")[3:].isdigit())
        self.assertTrue(validate_license_number("ABC12345")[:3].isalpha())
        self.assertTrue(validate_license_number("ABC12345")[:3].isupper())
