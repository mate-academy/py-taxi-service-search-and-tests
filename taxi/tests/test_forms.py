from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm


class FormTest(TestCase):
    def test_validate_license_number(self) -> None:
        form_data = {
            "license_number": "SDF12345"
        }
        form = DriverLicenseUpdateForm(form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_with_incorrect_data_license_number(self) -> None:
        form_data = {
            "license_number": "SF12345"
        }
        form = DriverLicenseUpdateForm(form_data)

        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)
