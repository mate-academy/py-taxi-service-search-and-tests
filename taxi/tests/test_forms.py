from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_driver_form_with_additional_info(self):
        form_data = {
            "username": "new_user",
            "password1": "user1234@",
            "password2": "user1234@",
            "license_number": "QWE12345",
            "first_name": "UserF",
            "last_name": "UserL",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)

    def test_validation_of_creating_license_number_first_3_symbols(self):
        form_data = {
            "username": "test_user",
            "password": "test1234@",
            "license_number": "1DM56921"
        }

        form = DriverCreationForm(data=form_data)

        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"]
        )
