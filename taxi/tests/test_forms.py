from django.test import TestCase
from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "Test password123",
            "password2": "Test password123",
            "first_name": "first_name",
            "last_name": "last_name",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)

        if not form.is_valid():
            print("Form errors:", form.errors)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
