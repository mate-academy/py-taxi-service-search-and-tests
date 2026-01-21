from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_is_valid(self) -> None:
        form_data = {
            "username": "new_user",
            "password1": "test123user",
            "password2": "test123user",
            "license_number": "DDD88888",
            "first_name": "test_first",
            "last_name": "test_last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update_license_form(self) -> None:
        form_data = {"license_number": "DDD00000"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
