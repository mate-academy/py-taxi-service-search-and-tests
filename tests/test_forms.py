from django.test import TestCase
from taxi.forms import DriverCreationForm


class DriverCreationFormTest(TestCase):
    def test_form_is_valid_with_all_required_fields(self):
        form_data = {
            "username": "new_user",
            "password1": "securepassword",
            "password2": "securepassword",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())

        expected_data = {
            key: form.cleaned_data[key] for key in form_data
        }
        self.assertEqual(expected_data, form_data)
