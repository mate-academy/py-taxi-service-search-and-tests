from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm, SearchForm


class SearchFormTest(TestCase):
    def test_empty_value_is_valid(self):
        self.assertTrue(SearchForm(data={"searched_value": ""}).is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_valid_license(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())

    def test_invalid_licenses(self):
        for value in [
            "abc12345",
            "AB123456",
            "ABC1234X",
            "ABC123456",
            "ABC1234",
        ]:
            with self.subTest(license_number=value):
                form = DriverLicenseUpdateForm(data={"license_number": value})
                self.assertFalse(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_license_validation_is_applied(self):
        data = {
            "username": "new_driver",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "abc12345",  # lowercase -> invalid
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
