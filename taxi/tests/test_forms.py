from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverFormTest(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "new_driver",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_invalid_license_number(self):
        form_data = {
            "username": "new_driver",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "invalidlicense",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
