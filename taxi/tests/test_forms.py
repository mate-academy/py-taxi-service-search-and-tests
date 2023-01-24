from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTest(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name(self):
        form_data = {
            "username": "new_driver",
            "password1": "user123test",
            "password2": "user123test",
            "license_number": "ABC12345",
            "first_name": "User",
            "last_name": "Shift",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
