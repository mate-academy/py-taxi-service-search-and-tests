from django.test import TestCase

from taxi.forms import DriverCreationForm


class TestForms(TestCase):
    def test_check_user_creation_form_with_valid_data(self):
        user_data = {
            "username": "testuser",
            "password1": "Qwerty123",
            "password2": "Qwerty123",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "TES12345",
        }
        form = DriverCreationForm(data=user_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, user_data)
