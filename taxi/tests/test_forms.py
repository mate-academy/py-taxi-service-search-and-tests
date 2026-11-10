from django.test import TestCase

from taxi.forms import (
    CarSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
)


class DriverCreationFormTests(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "new_user",
            "password1": "User12345test",
            "password2": "User12345test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345",
        }

    def test_form_with_valid_data(self) -> None:
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["license_number"], "ABC12345")

    def test_form_rejects_invalid_license_number(self) -> None:
        self.form_data["license_number"] = "abc12345"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_form_rejects_different_passwords(self) -> None:
        self.form_data["password2"] = "Other12345test"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def test_license_number_validation(self) -> None:
        cases = {
            "ABC12345": True,
            "ABC1234": False,
            "ABC123456": False,
            "AB123456": False,
            "abc12345": False,
            "ABCD2345": False,
        }
        for license_number, expected in cases.items():
            with self.subTest(license_number=license_number):
                form = DriverLicenseUpdateForm(
                    data={"license_number": license_number}
                )
                self.assertEqual(form.is_valid(), expected)


class SearchFormTests(TestCase):
    def test_search_form_is_valid_when_empty(self) -> None:
        self.assertTrue(CarSearchForm(data={"model": ""}).is_valid())
