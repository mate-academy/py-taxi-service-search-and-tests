from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer


class FormTest(TestCase):
    INVALID_LICENCE_NUMBERS = [
        ("A*D12345", "First 3 characters should be uppercase letters"),
        ("ASD123*5", "Last 5 characters should be digits"),
        ("ASD1234", "License number should consist of 8 characters"),
        ("ASD123456", "License number should consist of 8 characters"),
    ]

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="United Kingdom",
        )

        self.driver = get_user_model().objects.create_user(
            username="tester",
            password="testpassword123",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            license_number="ABC12345",
        )

        self.car_data = {
            "model": "model123",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id],
        }

        self.driver_data = {
            "username": "username",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "license_number": "QWE12345",
            "first_name": "first_name",
            "last_name": "last_name",
        }

    def test_car_form_valid(self):
        form = CarForm(data=self.car_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], self.car_data["model"])

    def test_driver_creation_form_valid(self):
        form = DriverCreationForm(data=self.driver_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.driver_data)

    def test_driver_creation_form_missing_custom_required_field(self):
        self.driver_data.pop("license_number")
        form = DriverCreationForm(data=self.driver_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_licence_number_validation(self):
        for license_number, error_msg in self.INVALID_LICENCE_NUMBERS:
            self.driver_data["license_number"] = license_number
            form = DriverCreationForm(data=self.driver_data)

            self.assertFalse(form.is_valid(), msg=error_msg)

    def test_driver_update_licence_form_valid(self):
        licence = "ASD12345"
        form = DriverLicenseUpdateForm(data={"license_number": licence})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["license_number"], licence)

    def test_driver_update_licence_form_validation(self):
        for license_number, error_msg in self.INVALID_LICENCE_NUMBERS:
            form = DriverLicenseUpdateForm(
                data={"license_number": license_number}
            )

            self.assertFalse(form.is_valid(), msg=error_msg)
