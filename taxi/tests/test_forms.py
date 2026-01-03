from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "Test12345",
            "password2": "Test12345",
            "first_name": "Test",
            "last_name": "User",
            "license_number": "ABC12345",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"],
            "ABC12345"
        )
