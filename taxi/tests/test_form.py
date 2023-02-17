from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)


class DriverFormTest(TestCase):
    def test_driver_creation_with_lowercase_license(self) -> None:
        data = {
            "username": "Test_driver",
            "password1": "driver-password",
            "password2": "driver-password",
            "license_number": "aaa11111",
        }
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_with_correct_license_number(self) -> None:
        data = {
            "username": "Test_driver",
            "password1": "driver-password",
            "password2": "driver-password",
            "license_number": "AAA11111",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_license_update_form_with_wrong_len(self) -> None:
        data = {
            "username": "Test_driver",
            "password1": "driver-password",
            "password2": "driver-password",
            "license_number": "AAA111111111111",
        }
        form = DriverLicenseUpdateForm(data=data)

        self.assertFalse(form.is_valid())

    def test_license_update_form_without_digits(self) -> None:
        data = {
            "username": "Test_driver",
            "password1": "driver-password",
            "password2": "driver-password",
            "license_number": "AAABBBCC",
        }
        form = DriverLicenseUpdateForm(data=data)

        self.assertFalse(form.is_valid())

    def test_driver_search_form(self):
        data = {"username": "a"}
        form = DriverSearchForm(data=data)

        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        data = {"model": "m"}
        form = CarSearchForm(data=data)

        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        data = {"name": "x"}
        form = ManufacturerSearchForm(data=data)

        self.assertTrue(form.is_valid())
