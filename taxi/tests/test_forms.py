from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTest(TestCase):
    def test_driver_with_first_name_last_name_and_license_number_is_valid(self):  # noqa
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "New",
            "last_name": "User",
            "license_number": "TTT12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_update_driver_with_first_name_last_name_and_license_number_is_valid(self):  # noqa
        form_data = {
            "license_number": "TTT12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
