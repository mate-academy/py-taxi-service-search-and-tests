from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarSearchForm
)


class FormsTest(TestCase):

    def get_valid_form_data(self, custom_license="AAA11111"):
        return {
            "username": "new_driver",
            "password1": "driver12345",
            "password2": "driver12345",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": custom_license,
        }

    def test_driver_creation_form_is_valid(self):
        form_data = self.get_valid_form_data()
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_form_license_wrong_length(self):
        form_data = self.get_valid_form_data(custom_license="AA111")
        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "License number should consist of 8 characters",
            form.errors["license_number"]
        )

    def test_driver_form_license_first_3_not_uppercase_letters(self):
        # Малі літери на початку
        form_data = self.get_valid_form_data(custom_license="aaA11111")
        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "First 3 characters should be uppercase letters",
            form.errors["license_number"]
        )

    def test_driver_form_license_last_5_not_digits(self):
        # Літера наприкінці
        form_data = self.get_valid_form_data(custom_license="AAA1111A")
        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "Last 5 characters should be digits",
            form.errors["license_number"]
        )

    def test_license_update_form_valid(self):
        form_data = {"license_number": "BBB22222"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form_is_optional(self):
        form = CarSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())
