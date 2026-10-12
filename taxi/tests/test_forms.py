from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "test",
            "password1": "X9!qL2#vR7@k",
            "password2": "X9!qL2#vR7@k",
            "first_name": "First driver",
            "last_name": "Last driver",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_invalid_license_length(self):
        form_data = {
            "username": "test",
            "password1": "X9!qL2#vR7@k",
            "password2": "X9!qL2#vR7@k",
            "first_name": "First driver",
            "last_name": "Last driver",
            "license_number": "ABC1234",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_invalid_license_case(self):
        form_data = {
            "username": "test",
            "password1": "X9!qL2#vR7@k",
            "password2": "X9!qL2#vR7@k",
            "first_name": "First driver",
            "last_name": "Last driver",
            "license_number": "AbC12345",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_invalid_license_letters(self):
        form_data = {
            "username": "test",
            "password1": "X9!qL2#vR7@k",
            "password2": "X9!qL2#vR7@k",
            "first_name": "First driver",
            "last_name": "Last driver",
            "license_number": "A1C12345",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_invalid_license_digits(self):
        form_data = {
            "username": "test",
            "password1": "X9!qL2#vR7@k",
            "password2": "X9!qL2#vR7@k",
            "first_name": "First driver",
            "last_name": "Last driver",
            "license_number": "ABC1234X",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_passwords_do_not_match(self):
        form_data = {
            "username": "test",
            "password1": "X9!qL2#vR7@k",
            "password2": "DifferentPass123!",
            "first_name": "First driver",
            "last_name": "Last driver",
            "license_number": "ABC12345",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
