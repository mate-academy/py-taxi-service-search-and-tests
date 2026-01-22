from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
)
from taxi.models import Manufacturer


class CarFormTest(TestCase):
    def test_car_form_valid(self):
        user = get_user_model().objects.create_user(
            username="testuser",
            password="test_Password1"
        )

        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="USA",
        )

        car_data = {
            "model": "BMW",
            "manufacturer": manufacturer.id,
            "drivers": [user],
        }

        form = CarForm(data=car_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self):
        form = CarForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "testdriver",
            "password1": "testPassword1",
            "password2": "testPassword1",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "Driver"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license_number(self):
        form_data = {
            "username": "testdriver",
            "password1": "testPassword1",
            "password2": "testPassword1",
            "license_number": "11111",
            "first_name": "Test",
            "last_name": "Driver"
        }

        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_valid(self):
        form_data = {
            "license_number": "AAA98765"
        }

        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        form_data = {
            "license_number": "abcccdda"
        }

        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
