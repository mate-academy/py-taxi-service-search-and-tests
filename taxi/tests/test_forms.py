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

    def test_license_number_should_be_not_more_than_8(self) -> None:
        form_data = {
            "license_number": "SF1234512467u8"
        }
        form = DriverLicenseUpdateForm(form_data)

        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)

    def test_license_number_should_be_not_less_than_8(self) -> None:
        form_data = {
            "license_number": "SF123"
        }
        form = DriverLicenseUpdateForm(form_data)

        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)

    def test_license_first_3_letter_should_be_uppercase(self) -> None:
        form_data = {
            "license_number": "sdf12345"
        }
        form = DriverLicenseUpdateForm(form_data)

        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)

    def test_license_number_last_5_characters_should_be_numbers(self) -> None:
        form_data = {
            "license_number": "SDF1D3DF"
        }
        form = DriverLicenseUpdateForm(form_data)

        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)
