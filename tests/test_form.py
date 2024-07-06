from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    CarModelSearchForm,
    DriverCreationForm,
    DriverUsernameSearchForm,
    DriverLicenseUpdateForm,
    ManufacturerNameSearchForm
)


class FormTests(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234",
        )

    def test_driver_creation_form(self):
        form = DriverCreationForm(
            data={
                "username": "test_username",
                "password1": "test_password",
                "password2": "test_password",
                "license_number": "VPN99999",
                "first_name": "test_first",
                "last_name": "test_last"
            }
        )
        self.assertTrue(form.is_valid())

    def test_driver_search_form(self):
        form = DriverUsernameSearchForm(
            data={
                "username": "test_username"
            }
        )
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form(self):
        form = DriverLicenseUpdateForm(
            data={
                "license_number": "VPN99999"
            }
        )
        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        form = CarModelSearchForm(
            data={
                "model": "test"
            }
        )
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form = ManufacturerNameSearchForm(
            data={
                "name": "Test"
            }
        )
        self.assertTrue(form.is_valid())
