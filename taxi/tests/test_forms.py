from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Driver


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "QWE12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_wrong_length_is_invalid(self):
        form_data = {
            "username": "user1",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "Test",
            "last_name": "User",
            "license_number": "ABC123",  # 6 chars
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "License number should consist of 8 characters",
            form.errors["license_number"]
        )

    def test_license_number_wrong_format_letters(self):
        form_data = {
            "username": "user1",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "Test",
            "last_name": "User",
            "license_number": "abc12345",  # lowercase
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "First 3 characters should be uppercase letters",
            form.errors["license_number"]
        )

    def test_license_number_wrong_digits(self):
        form_data = {
            "username": "user1",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "Test",
            "last_name": "User",
            "license_number": "ABC12X45",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "Last 5 characters should be digits",
            form.errors["license_number"]
        )


class DriverLicenseUpdateFormTests(TestCase):
    def test_valid_license_update(self):
        driver = Driver.objects.create_user(
            username="driver1",
            password="test12345",
            license_number="ABC12345"
        )

        form = DriverLicenseUpdateForm(
            data={"license_number": "DEF54321"},
            instance=driver
        )

        self.assertTrue(form.is_valid())

    def test_invalid_license_update(self):
        driver = Driver.objects.create_user(
            username="driver1",
            password="test12345",
            license_number="ABC12345"
        )

        form = DriverLicenseUpdateForm(
            data={"license_number": "invalid"},
            instance=driver
        )

        self.assertFalse(form.is_valid())
