from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    CarSearchForm,
)

DRIVER_FORM_DATA = {
    "username": "driver",
    "license_number": "AAA00000",
    "first_name": "John",
    "last_name": "Mills",
    "password1": "123password123",
    "password2": "123password123",
}


class FormsTests(TestCase):

    def test_driver_creation_form_all_data_valid(self) -> None:
        form = DriverCreationForm(data=DRIVER_FORM_DATA)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, DRIVER_FORM_DATA)

    def test_driver_creation_form_license_number_short(self) -> None:
        DRIVER_FORM_DATA["license_number"] = "AAA00"
        form = DriverCreationForm(DRIVER_FORM_DATA)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "license_number",
            "License number should consist of 8 characters",
        )

    def test_driver_creation_form_license_number_first_3(self) -> None:
        DRIVER_FORM_DATA["license_number"] = "AA000000"
        form = DriverCreationForm(DRIVER_FORM_DATA)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "license_number",
            "First 3 characters should be uppercase letters",
        )

    def test_driver_creation_form_license_number_last_5(self) -> None:
        DRIVER_FORM_DATA["license_number"] = "AAA0000f"
        form = DriverCreationForm(DRIVER_FORM_DATA)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "license_number",
            "Last 5 characters should be digits",
        )
