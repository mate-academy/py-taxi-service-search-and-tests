from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "miwa_dr",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "Miwa",
            "last_name": "Vovchok",
            "license_number": "NNN78555",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_not_valid(self):
        form_data = {
            "username": "driver",
            "password1": "fdbgfdbx",
            "password2": "fdbgfdbx",
            "license_number": "",
            "first_name": "",
            "last_name": "",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_license_update_form_valid(self):
        driver = get_user_model().objects.create(username="driver")
        form = DriverLicenseUpdateForm(
            data={"license_number": "MVO45896"},
            instance=driver
        )
        self.assertTrue(form.is_valid())
