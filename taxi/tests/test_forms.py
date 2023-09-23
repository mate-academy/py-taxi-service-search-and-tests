from django.test import TestCase

from taxi.forms import DriverCreationForm, validate_license_number


class DriverCreationFormTests(TestCase):
    def test_license_number_validation(self):
        tests = [
            ("AAA123456", False),
            ("AAA1234", False),
            ("A0A00000", False),
            ("AAA00A00", False),
            ("AAA00000", True),
        ]
        for license_number, expected_result in tests:
            form_data = {
                "username": "test.driver",
                "license_number": license_number,
                "password1": "test_password",
                "password2": "test_password",
            }
            form = DriverCreationForm(data=form_data)
            self.assertEquals(form.is_valid(), expected_result)

    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "test.driver",
            "license_number": "ADC12345",
            "first_name": "test_first",
            "last_name": "test_last",
            "password1": "test_password",
            "password2": "test_password",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)
