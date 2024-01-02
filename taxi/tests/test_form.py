from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class TestDriverCreationForm(TestCase):
    def setUp(self):
        self.form_date = {
            "username": "test_user_name",
            "password1": "test1234567",
            "password2": "test12345998",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }

    def test_drivers_creation_form_with_additional_fields(self):
        self.form_date["license_number"] = "AGC12345"
        form = DriverCreationForm(data=self.form_date)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_date)

    def test_valid_license_number(self):
        license_numbers = [
            "aBC12345", "abc", "ABC123n5", "abc12345", "ABC1234567"
        ]
        for license_number in license_numbers:
            self.form_date["license_number"] = license_number
            form = DriverCreationForm(data=self.form_date)
            self.assertFalse(form.is_valid())

    def test_update_license_number(self):
        get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
            license_number="ABC12345"
        )
        license_numbers = [
            "aBC12345", "abc", "ABC123d5", "abc12345", "ABC1234567"
        ]
        for license_num in license_numbers:
            form = DriverLicenseUpdateForm(
                data={"license_number": license_num}
            )
            self.assertFalse(form.is_valid())
