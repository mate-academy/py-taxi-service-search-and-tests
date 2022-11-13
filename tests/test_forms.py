from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_driver_create_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "test123test",
            "password2": "test123test",
            "first_name": "Test1",
            "last_name": "Test2",
            "license_number": "AAA12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_validation(self):
        incorrect_license_number = [
            "AA123456",
            "AAA1234",
            "AAA1234A",
            "AAa12345"
        ]

        for number in incorrect_license_number:
            form = DriverLicenseUpdateForm({"license_number": number})

            self.assertFalse(form.is_valid())
