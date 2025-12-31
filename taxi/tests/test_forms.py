from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
)


class FormTests(TestCase):

    def test_driver_creation_form(self) -> None:
        form_data = {
            "username": "testuser",
            "license_number": "TST12345",
            "first_name": "Test first",
            "last_name": "Test last",
            "password1": "test12345",
            "password2": "test12345"
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_number_update_form(self) -> None:
        form_data = {
            "license_number": "TSS12344"
        }
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
