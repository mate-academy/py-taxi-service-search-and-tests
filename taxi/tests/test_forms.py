from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_driver_license_update_form(self):
        valid_form_data = {
            "license_number": "AVC12345"
        }
        invalid_form_data = [
            {"license_number": "AVc12345"},
            {"license_number": "1VC12345"},
            {"license_number": "AVC12A45"},
        ]
        form = DriverLicenseUpdateForm(data=valid_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, valid_form_data)

        for invalid_license_number in invalid_form_data:
            form = DriverLicenseUpdateForm(
                data=invalid_license_number
            )
            self.assert_form_is_not_valid(form)

    def assert_form_is_not_valid(self, form):
        self.assertFalse(form.is_valid())
