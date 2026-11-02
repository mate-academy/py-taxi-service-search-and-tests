from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_license_number_with_wrong_length(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "TCP333333"}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_with_all_numbers(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "33312345"}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_with_all_letters(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "TCPQWERT"}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_with_small_leterrs(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "tcp33333"}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_valid_license_number(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "TCP33333"}
        )

        self.assertTrue(form.is_valid())
