from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_lisence_and_name(self):
        from_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TES12345"
        }
        wrong_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TES123456"
        }
        form = DriverCreationForm(data=from_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, from_data)
        form = DriverCreationForm(data=wrong_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_update_form(self):
        from_data = {
            "license_number": "TES12345"
        }
        wrong_data = {
            "license_number": "TES123456"
        }
        form = DriverLicenseUpdateForm(data=from_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, from_data)
        form = DriverLicenseUpdateForm(data=wrong_data)
        self.assertFalse(form.is_valid())
