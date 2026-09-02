from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm


class DriverFormTests(TestCase):
    def test_driver_license_with_lowercase_letters_is_invalid(self):
        form = DriverLicenseUpdateForm(
            data={
                "license_number": "abc12345"
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
