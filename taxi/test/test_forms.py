from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_custom_is_valid(self) -> None:
        form_data = {
            "username": "test_user",
            "password1": "12345test.",
            "password2": "12345test.",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
