from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm, DriverCreationForm


class LicenseNumberValidationTests(TestCase):
    @staticmethod
    def update_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    def test_license_number_is_valid(self):
        self.assertTrue(self.update_form("ABC12345").is_valid())

    def test_license_number_min_length_is_8(self):
        self.assertFalse(self.update_form("ABC1234").is_valid())

    def test_license_number_max_length_is_8(self):
        self.assertFalse(self.update_form("ABC123456").is_valid())

    def test_3_first_characters_should_be_uppercase_letters(self):
        self.assertFalse(self.update_form("cba12345").is_valid())

    def test_5_last_characters_should_be_numbers(self):
        self.assertFalse(self.update_form("ABC12o45").is_valid())


class DriverCreationTest(TestCase):
    def test_create_driver_with_custom_fields(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "license_number": "ABC12345",
            "first_name": "Test First",
            "last_name": "Test Last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
