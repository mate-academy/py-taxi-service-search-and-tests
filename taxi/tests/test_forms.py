from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreationFormTests(TestCase):
    def test_validate_license_number(self):
        tests = [
            ("ABC123456", False),
            ("ABC1234", False),
            ("AB123456", False),
            ("ABC12D34", False),
            ("ABC12345", True),
        ]
        for license_number, expected_result in tests:
            form_data = {
                "username": "test.driver",
                "license_number": license_number,
                "password1": "testpassword",
                "password2": "testpassword",
            }
            form = DriverCreationForm(data=form_data)
            self.assertEquals(form.is_valid(), expected_result)

    def test_driver_creation_when_all_data_is_valid(self):
        form_data = {
            "username": "test.user",
            "license_number": "ABC12345",
            "first_name": "testfirst",
            "last_name": "testlast",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)


class DriverLicenseUpdateFormTest(TestCase):

    def test_valid_form(self) -> None:
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_more_than_8_characters(self) -> None:
        form = DriverLicenseUpdateForm(data={"license_number": "ABC123456"})
        self.assertFalse(form.is_valid())

    def test_letters_in_lower_case(self) -> None:
        form = DriverLicenseUpdateForm(data={"license_number": "abc12345"})
        self.assertFalse(form.is_valid())

    def test_more_than_3_letters(self) -> None:
        form = DriverLicenseUpdateForm(data={"license_number": "ABCD12345"})
        self.assertFalse(form.is_valid())
