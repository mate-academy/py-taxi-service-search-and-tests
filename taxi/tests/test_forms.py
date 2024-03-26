from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarSearchForm,
    ManufacturerSearchForm,
    DriverSearchForm,
)


class FormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="password"
        )

    def test_driver_creation_form(self):
        form_data = {
            "username": "testqewrt",
            "password1": "test_123456",
            "password2": "test_123456",
            "license_number": "ABC12345",
            "first_name": "test",
            "last_name": "test",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form(self):
        form_data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        form_data = {
            "model": "Test",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_valid(self):
        form_data = {
            "name": "Test",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_valid(self):
        form_data = {
            "username": "test",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
