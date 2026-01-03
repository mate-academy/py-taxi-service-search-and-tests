from django.test import TestCase

from taxi.forms import (DriverCreationForm)

DRIVER_FORM_DATA = {
    "username": "driver_username",
    "license_number": "AAA12345",
    "first_name": "Bob",
    "last_name": "Marley",
    "password1": "password123!",
    "password2": "password123!",
}


class FormsTests(TestCase):

    def test_driver_creation_form_all_data_valid(self) -> None:
        """
        Test that driver created with valid data!
        """
        form = DriverCreationForm(data=DRIVER_FORM_DATA)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, DRIVER_FORM_DATA)

    def test_driver_creation_form_license_number_short(self) -> None:
        """
        Test that driver does not create with short license number!
        """
        DRIVER_FORM_DATA["license_number"] = "AAA12"
        form = DriverCreationForm(DRIVER_FORM_DATA)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "license_number",
            "License number should consist of 8 characters",
        )

    def test_driver_creation_form_license_number_first_3(self) -> None:
        """
        Test that driver does not create with no three uppercase letter
        at the beginning of the license number!
        """
        DRIVER_FORM_DATA["license_number"] = "AA123456"
        form = DriverCreationForm(DRIVER_FORM_DATA)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "license_number",
            "First 3 characters should be uppercase letters",
        )

    def test_driver_creation_form_license_number_last_5(self) -> None:
        """
        Test that driver does not create with no five digits
        at the end of the license number!
        """
        DRIVER_FORM_DATA["license_number"] = "AAA123a5"
        form = DriverCreationForm(DRIVER_FORM_DATA)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "license_number",
            "Last 5 characters should be digits",
        )
