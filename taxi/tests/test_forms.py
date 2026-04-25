from django.test import TestCase

from taxi.forms import (
    SearchManufacturerForm,
    SearchCarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    SearchDriverForm,
)


class SearchManufacturerFormTest(TestCase):
    def test_form_is_valid(self):
        data = {
            "name": "BMW"
        }
        self.assertTrue(SearchManufacturerForm(data=data).is_valid())


class SearchCarFormTest(TestCase):
    def test_form_is_valid(self):
        data = {
            "model": "X3"
        }
        self.assertTrue(SearchCarForm(data=data).is_valid())


class SearchDriverFormTest(TestCase):
    def test_form_is_valid(self):
        data = {
            "username": "TestUser"
        }
        self.assertTrue(SearchDriverForm(data=data).is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_validation_license_number_with_correct_value(self):
        data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_validation_license_number_with_incorrect_length_value(self):
        data = {"license_number": "ABC123456"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_validation_license_number_with_lowercase_letters_in_begin_value(
            self
    ):
        data = {"license_number": "abc12345"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_validation_license_number_with_incorrect_number_of_digits(self):
        data = {"license_number": "ABC1234"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_validation_license_number_with_incorrect_number_letters_in_begin(
        self
    ):
        data = {"license_number": "AB123456"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())


class DriverCreationFormTest(DriverLicenseUpdateFormTest, TestCase):

    def test_form_is_valid(self):
        data = {
            "username": "TestUser",
            "first_name": "Test",
            "last_name": "User",
            "license_number": "ABC12345",
            "password1": "Testpassword",
            "password2": "Testpassword",

        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)

    def test_form_is_valid_with_incorrect_license_number(self):
        data = {
            "username": "TestUser",
            "first_name": "Test",
            "last_name": "User",
            "license_number": "AB12345",
            "password1": "Testpassword",
            "password2": "Testpassword",

        }
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())
