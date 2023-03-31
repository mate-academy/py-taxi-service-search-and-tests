from django.test import TestCase


from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTest(TestCase):

    def test_driver_creation_form_with_first_name_last_name_licence(self):
        form_data = {
            "username": "TestUser",
            "password1": "qwer1234!",
            "password2": "qwer1234!",
            "license_number": "ASD12341",
            "first_name": "test_name",
            "last_name": "test_last_name"

        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_check_license_validation(self):
        form_7_characters = DriverLicenseUpdateForm(
            data={"license_number": "ASD1231"}
        )
        form_just_digits = DriverLicenseUpdateForm(
            data={"license_number": "12312312"}
        )
        form_just_letters = DriverLicenseUpdateForm(
            data={"license_number": "AARDVARK"}
        )

        self.assertFalse(form_7_characters.is_valid())
        self.assertFalse(form_just_digits.is_valid())
        self.assertFalse(form_just_letters.is_valid())
