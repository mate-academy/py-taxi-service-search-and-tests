from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_driver_license(self):
        form_data = {
            "username": "test",
            "license_number": "TTT56566",
            "first_name": "Jake",
            "last_name": "Black",
            "password1": "veryhardpassword123",
            "password2": "veryhardpassword123",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_with_lowercase_letters_driver_license(self):
        form_data = {
            "username": "test",
            "license_number": "ttt56566",
            "password1": "veryhardpassword123",
            "password2": "veryhardpassword123",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_driver_creation_form_with_incorrect_license_number(self):
        form_data = {
            "username": "test",
            "license_number": "ttt5652266",
            "password1": "veryhardpassword123",
            "password2": "veryhardpassword123",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_driver_creation_form_with_one_letter_in_driver_license(self):
        form_data = {
            "username": "test",
            "license_number": "t2222222",
            "password1": "veryhardpassword123",
            "password2": "veryhardpassword123",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
