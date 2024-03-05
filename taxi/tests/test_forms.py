from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class TestForms(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_driver_creation_form_valid_data(self):
        form_data = {
            "username": "New_driver",
            "password1": "new_drivers_password",
            "password2": "new_drivers_password",
            "license_number": "ASD12345",
            "first_name": "New",
            "last_name": "Driver",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_data(self):
        form_data = {
            "username": "New_driver",
            "password1": "new_drivers_password",
            "password2": "different_password",
            "license_number": "ASD12345",
            "first_name": "New",
            "last_name": "Driver",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_driver_license_update_form_valid_data(self):
        form_data = {"license_number": "ASD12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid_data(self):
        form_data = {"license_number": "InvalidLicenseNumber"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
