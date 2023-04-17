from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverCreationFormTest(TestCase):
    def test_driver_create_form_license_number_label(self):
        form = DriverCreationForm()
        self.assertTrue(
            (form.fields["license_number"].label is None
             or form.fields["license_number"].label == "License number")
        )

    def test_driver_create_form_license_number_length_is_not_8(self):
        data = {
            "username": "test_user",
            "license_number": "ABC123456",
            "password1": "test12345test",
            "password2": "test12345test",
            "first_name": "Test",
            "last_name": "Test"
        }

        form = DriverCreationForm(data)
        self.assertFalse(form.is_valid())

    def test_driver_create_form_license_number_first_3_is_not_upper(self):
        data = {
            "username": "test_user",
            "license_number": "abc12345",
            "password1": "test12345test",
            "password2": "test12345test",
            "first_name": "Test",
            "last_name": "Test"
        }

        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_driver_create_form_license_number_last_5_is_not_digits(self):
        data = {
            "username": "test_user",
            "license_number": "abcd1234",
            "password1": "test12345test",
            "password2": "test12345test",
            "first_name": "Test",
            "last_name": "Test"
        }

        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_driver_create_form_license_number_is_valid(self):
        data = {
            "username": "test_user",
            "license_number": "ABC12345",
            "password1": "test12345test",
            "password2": "test12345test",
            "first_name": "Test",
            "last_name": "Test"
        }

        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
