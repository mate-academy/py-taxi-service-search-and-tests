from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "license_number": "ABC23456",
            "first_name": "Test",
            "last_name": "User",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        expected_cleaned = {
            "username": "testuser",
            "license_number": "ABC23456",
            "first_name": "Test",
            "last_name": "User",
        }
        actual_subset = {
            key: form.cleaned_data.get(key) for key in expected_cleaned
        }
        self.assertEqual(actual_subset, expected_cleaned)
