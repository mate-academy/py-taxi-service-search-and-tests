from django.test import TestCase

from taxi.forms import DriverCreationForm


class TestDriverCreationForm(TestCase):
    def test_driver_creation_form_with_license_number_first_name_and_last_name(
            self):
        form_data = {
            "username": "test_user",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "JOY26458",
            "first_name": "John",
            "last_name": "Doe",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
