from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number
)


class DriverFormsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="qwerty",
            license_number="QWE12345"
        )

    def test_driver_creation_form_valid_data(self):
        form_data = {
            "username": "driver",
            "password1": "dri123aq",
            "password2": "dri123aq",
            "license_number": "ZXC12345",
            "first_name": "Carl",
            "last_name": "Bon",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_data(self):
        form_data = {
            "username": "driver",
            "password1": "dri123aq",
            "password2": "dri123aq",
            "license_number": "12345678",
            "first_name": "Carl",
            "last_name": "Bon",
        }
        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_driver_license_update_form_valid_data(self):
        form_data = {"license_number": "ASD12345"}
        form = DriverLicenseUpdateForm(data=form_data, instance=self.user)

        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid_data(self):
        form_data = {"license_number": "12345678"}
        form = DriverLicenseUpdateForm(data=form_data, instance=self.user)

        self.assertFalse(form.is_valid())

    def test_validate_license_number_valid(self):
        valid_license = "QWE12345"

        self.assertEqual(validate_license_number(valid_license), valid_license)

    def test_validate_license_number_invalid(self):
        invalid_license = "12345678"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license)
