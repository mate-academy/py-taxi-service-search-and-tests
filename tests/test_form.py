from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarSearchForm,
    ManufacturerSearchForm,
    DriverSearchForm
)


class FormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password"
        )

    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "test_driver",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "Driver",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_valid(self):
        form_data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form_valid(self):
        form_data = {
            "model": "Test Model",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_valid(self):
        form_data = {
            "name": "Test Manufacturer",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_valid(self):
        form_data = {
            "username": "test_username",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_license_number(self):
        invalid_license_numbers = ["12345", "ABCDEFGH", "ABC1234", "ABC123456"]
        for license_number in invalid_license_numbers:
            form_data = {
                "license_number": license_number,
            }
            form = DriverCreationForm(data=form_data)
            self.assertFalse(form.is_valid())
