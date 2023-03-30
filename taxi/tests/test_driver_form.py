from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm, DriverCreationForm


class DriverFormTests(TestCase):

    def driver_creation_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12345",
            "password2": "user12345",
            "first_name": "first_name",
            "last_name": "last_name",
            "license_number": "KIA12235"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class ValidLicenseNumberFormTests(TestCase):
    @staticmethod
    def create_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    def test_validation_license_number_with_valid_data(self):
        self.assertTrue(self.create_form("KIA34567").is_valid())

    def test_length_of_license_number_should_be_not_more_than_8(self):
        self.assertFalse(self.create_form("KIA345679").is_valid())

    def test_length_of_license_number_should_be_not_less_than_8(self):
        self.assertFalse(self.create_form("KIA3456").is_valid())

    def test_first_3_characters_should_be_uppercase_letters(self):
        self.assertFalse(self.create_form("KI734567").is_valid())

    def test_last_5_characters_should_be_be_digits(self):
        self.assertFalse(self.create_form("KIAI4567").is_valid())
