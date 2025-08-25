from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Driver


class FormTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(
            username="test_username",
            password="70Test123",
            license_number="TES12345"
        )

    def test_driver_creation_form(self):
        form_data = {
            "username": "test_username",
            "password1": "70Test123",
            "password2": "70Test123",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "TES12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_valid_driver_license_update_form(self):
        update_data = {
            "license_number": "NEW12345"
        }
        form = DriverLicenseUpdateForm(update_data, instance=self.driver)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["license_number"], "NEW12345")

    def test_invalid_length_driver_license_update_form(self):
        update_data = {
            "license_number": "NEW12345678"
        }
        form = DriverLicenseUpdateForm(update_data, instance=self.driver)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "License number should consist of 8 characters",
            form.errors["license_number"]
        )

    def test_invalid_three_uppercase_driver_license_update_form(self):
        update_data = {
            "license_number": "new12345"
        }
        form = DriverLicenseUpdateForm(update_data, instance=self.driver)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "First 3 characters should be uppercase letters",
            form.errors["license_number"]
        )

    def test_invalid_last_five_digits_driver_license_update_form(self):
        update_data = {
            "license_number": "NEW123as"
        }
        form = DriverLicenseUpdateForm(update_data, instance=self.driver)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Last 5 characters should be digits",
            form.errors["license_number"]
        )
