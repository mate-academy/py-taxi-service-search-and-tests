from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm


class LicenseNumberValidationTest(TestCase):
    def test_valid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "AAA23456"})

        self.assertTrue(form.is_valid())

    def test_invalid_license_number_length(self):
        form = DriverLicenseUpdateForm(data={"license_number": "AAA2345"})

        self.assertFalse(form.is_valid())

    def test_invalid_third_symbol(self):
        form = DriverLicenseUpdateForm(data={"license_number": "AA234548"})

        self.assertFalse(form.is_valid())

    def test_invalid_letter_register(self):
        form = DriverLicenseUpdateForm(data={"license_number": "AAa23454"})

        self.assertFalse(form.is_valid())

    def test_too_much_letters(self):
        form = DriverLicenseUpdateForm(data={"license_number": "AAAA3454"})

        self.assertFalse(form.is_valid())

    def test_too_much_digits(self):
        form = DriverLicenseUpdateForm(data={"license_number": "AAA434546"})

        self.assertFalse(form.is_valid())

    def test_empty_string(self):
        form = DriverLicenseUpdateForm(data={"license_number": ""})

        self.assertFalse(form.is_valid())
