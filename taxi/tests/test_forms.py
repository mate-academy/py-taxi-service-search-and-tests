from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_create_form_with_license_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_empty_is_valid(self):
        form_data = DriverCreationForm(data={})
        self.assertFalse(form_data.is_valid())

    def test_driver_creation_form_license_too_short(self):
        form_data = {
            "username": "new_user",
            "password": "user12test",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "license_number": "ABC1234",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_license_lowercase(self):
        form_data = {
            "username": "new_user",
            "password": "user12test",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "license_number": "abc12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_license_letters_at_end(self):
        form_data = {
            "username": "new_user",
            "password": "user12test",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "license_number": "ABCDEFGH",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
