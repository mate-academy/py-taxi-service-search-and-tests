from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreationFormTests(TestCase):
    def test_validate_license_number(self):
        tests = [
            ("AAA123456", False),
            ("AAA1234", False),
            ("A0A00000", False),
            ("AAA00A00", False),
            ("AAA00000", True),
        ]
        for license_number, expected_result in tests:
            form_data = {
                "username": "test2.driver",
                "license_number": license_number,
                "password1": "test_password",
                "password2": "test_password",
            }
            form = DriverCreationForm(data=form_data)
            self.assertEquals(form.is_valid(), expected_result)

    def test_driver_creation_form_with_license_and_full_name_is_valid(self):
        form_data = {
            "username": "test2.user",
            "license_number": "BDF98765",
            "first_name": "test_first",
            "last_name": "test_last",
            "password1": "test_password",
            "password2": "test_password",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)


class DriverLicenseUpdateFormTest(TestCase):
    def test_invalid_length_license_number(self) -> None:
        form = DriverLicenseUpdateForm(data={"license_number": "BDF987656"})
        self.assertFalse(form.is_valid())

    def test_invalid_upper_letters_quantity(self) -> None:
        form = DriverLicenseUpdateForm(data={"license_number": "BDа98765"})
        self.assertFalse(form.is_valid())

    def test_invalid_digits_quantity(self) -> None:
        form = DriverLicenseUpdateForm(data={"license_number": "BDFЕ8765"})
        self.assertFalse(form.is_valid())

    def test_valid_form(self) -> None:
        form_data = {"license_number": "BDF98765"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
