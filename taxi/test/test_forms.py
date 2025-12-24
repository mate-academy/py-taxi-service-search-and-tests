from django.test import TestCase

from taxi.forms import (
    CarModelSearchForm,
    DriverUsernameSearchForm,
    ManufacturerNameSearchForm,
    DriverLicenseUpdateForm
)


class FormTest(TestCase):
    def test_driver_username_search_form_is_valid(self):
        form_data = {
            "username": "reichikku",
        }
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_model_search_form_is_valid(self):
        form_data = {
            "model": "Subaru Forester",
        }
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_name_search_form_is_valid(self):
        form_data = {
            "name": "Subaru",
        }
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_license_number(self):
        form_data = {"license_number": "IOA22101"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_license_number_too_short(self):
        form_data = {"license_number": "AB123"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"]
        )

    def test_invalid_license_number_no_letters(self):
        form_data = {"license_number": "12345678"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"]
        )
