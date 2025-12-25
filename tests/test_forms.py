from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class CreationFormTest(TestCase):
    def test_driver_create_with_license_number_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "AAA12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class LicenseNumberValidationTests(TestCase):
    def test_driver_license_number_is_valid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "AAA12345"})
        self.assertTrue(form.is_valid())

    def test_driver_license_number_should_be_8_symbols(self):
        wrong_numbers = (
            "AAA1234",
            "A0A123456",
        )
        for number in wrong_numbers:
            form = DriverLicenseUpdateForm(data={"license_number": number})
            self.assertFalse(form.is_valid())

    def test_driver_license_number_start_with_letters(self):
        wrong_numbers = (
            "0AA12345",
            "A0A12345",
            "AA012345",
        )
        for number in wrong_numbers:
            form = DriverLicenseUpdateForm(data={"license_number": number})
            self.assertFalse(form.is_valid())

    def test_driver_license_number_ends_with_numbers(self):
        wrong_numbers = (
            "AAAa2345",
            "AAA1a345",
            "AAA12a45",
            "AAA123a5",
            "AAA1234a"
        )
        for number in wrong_numbers:
            form = DriverLicenseUpdateForm(data={"license_number": number})
            self.assertFalse(form.is_valid())

    def test_driver_license_letters_should_be_in_uppercase(self):
        form = DriverLicenseUpdateForm(data={"license_number": "aaa12345"})
        self.assertFalse(form.is_valid())
