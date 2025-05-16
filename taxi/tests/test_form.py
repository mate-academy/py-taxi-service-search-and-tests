from django.test import TestCase


from taxi.forms import DriverCreationForm


class TestForm(TestCase):
    def setUp(self):
        self.valid_data = {
            "username": "driver123",
            "password1": "verysecure123",
            "password2": "verysecure123",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "ABC12345",
        }

    def test_form_valid_with_correct_license_number(self):
        form = DriverCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_short_license_number(self):
        data = self.valid_data.copy()
        data["license_number"] = "AB123"
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertIn(
            "License number should consist of 8 characters",
            form.errors["license_number"]
        )

    def test_form_invalid_with_wrong_first_part(self):
        data = self.valid_data.copy()
        data["license_number"] = "abC12345"
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "First 3 characters should be uppercase letters",
            form.errors["license_number"]
        )

    def test_form_invalid_with_wrong_second_part(self):
        data = self.valid_data.copy()
        data["license_number"] = "ABC12A45"
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Last 5 characters should be digits",
            form.errors["license_number"]
        )
