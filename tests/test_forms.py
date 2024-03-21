from django.test import TestCase

from taxi.forms import (
    CarSearchForm,
    DriverCreationForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)


class TestForms(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "test",
            "password1": "test123123",
            "password2": "test123123",
            "first_name": "Bob",
            "last_name": "Marley",
            "license_number": "BMC12345",
        }

    def test_driver_creation_form_with_valid_data(self) -> None:
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_creation_form_with_invalid_license(self) -> None:
        for license_number in (
                "abc12343",
                "123qw52rty",
                "ABC123456",
                "ABC22WWW"
        ):
            self.form_data["license_number"] = license_number
            form = DriverCreationForm(data=self.form_data)
            self.assertFalse(form.is_valid())
