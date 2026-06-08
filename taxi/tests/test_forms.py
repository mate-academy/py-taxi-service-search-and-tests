from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
)

FORM_DATA = {
    "username": "new_user",
    "password1": "user12test",
    "password2": "user12test",
    "first_name": "Test first",
    "last_name": "Test last",
    "license_number": "ABC12345"
}


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_number(self):
        form = DriverCreationForm(data=FORM_DATA)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, FORM_DATA)

    def test_driver_update_form_with_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["license_number"], "ABC12345")

    def test_driver_creation_form_invalid_license_length(self):
        form = DriverCreationForm(
            data={**FORM_DATA, "license_number": "ABC1234"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_invalid_license_format(self):
        form = DriverCreationForm(
            data={**FORM_DATA, "license_number": "abc12345"}
        )
        self.assertFalse(form.is_valid())
