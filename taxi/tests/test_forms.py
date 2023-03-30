from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test_First",
            "last_name": "Test_Last",
            "license_number": "TST12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form.data)

    def test_driver_creation_form_with_invalid_license_number(self):
        invalid_licence_number = ["TS123", "tsa12345", "12345678", "tsa1234Q"]
        for number in invalid_licence_number:
            form_data = {
                "username": "new_user",
                "password1": "user123test",
                "password2": "user123test",
                "first_name": "Test_First",
                "last_name": "Test_Last",
                "license_number": number,
            }
            form = DriverCreationForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertNotEqual(form.cleaned_data, form.data)
