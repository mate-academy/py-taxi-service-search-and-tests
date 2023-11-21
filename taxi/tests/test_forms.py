from django.test import TestCase
from taxi.forms import DriverLicenseUpdateForm, DriverCreationForm


class FormTests(TestCase):
    def test_driver_creation_form_with_all_fields_is_valid(
            self
    ) -> None:
        form_data = {
            "username": "username",
            "password1": "bc1111ec",
            "password2": "bc1111ec",
            "license_number": "BBB22222",
            "first_name": "first_name",
            "last_name": "last_name",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_with_field_is_valid(self) -> None:
        form_data = {
            "license_number": "BBB22222",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_format(self) -> None:
        valid_license_numbers = [
            "BBB22222", "AAA12345", "BEK11111",
        ]
        invalid_license_numbers = [
            "A9999999",
            "BBBBBBB0",
            "AB111111",
            "111111AB",
            "BA1111AB",
            "11AAAA11",
            "11AA11AA",
            "AA11",
            "111A",
            "OAOAOK",
            "NEOK",
            "O",
        ]

        for license_number in valid_license_numbers:
            form_data = {
                "username": "username",
                "password1": "bc1111ec",
                "password2": "bc1111ec",
                "license_number": license_number,
                "first_name": "first_name",
                "last_name": "last_name",
            }
            form = DriverCreationForm(data=form_data)
            self.assertTrue(form.is_valid())

        for license_number in invalid_license_numbers:
            form_data = {
                "username": "username",
                "password1": "bc1111ec",
                "password2": "bc1111ec",
                "license_number": license_number,
                "first_name": "first_name",
                "last_name": "last_name",
            }
            form = DriverCreationForm(data=form_data)
            self.assertFalse(form.is_valid())
