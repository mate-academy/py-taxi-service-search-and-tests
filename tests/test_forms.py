from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.forms import DriverCreationForm, validate_license_number

User = get_user_model()


class ValidateLicenseNumberTest(TestCase):
    def test_license_number_valid(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_license_number_too_short(self):
        with self.assertRaises(ValidationError) as e:
            validate_license_number("ABC1234")
        self.assertIn("should consist of 8 characters", str(e.exception))

    def test_license_number_first_3_not_uppercase_letters(self):
        with self.assertRaises(ValidationError) as e:
            validate_license_number("AbC12345")
        self.assertIn(
            "First 3 characters should be uppercase letters", str(e.exception)
        )

    def test_license_number_last_5_not_digits(self):
        with self.assertRaises(ValidationError) as e:
            validate_license_number("ABC12A45")
        self.assertIn("Last 5 characters should be digits", str(e.exception))


class DriverCreationFormTest(TestCase):
    def test_form_has_fields(self):
        form = DriverCreationForm()
        self.assertIn("username", form.fields)
        self.assertIn("password1", form.fields)
        self.assertIn("password2", form.fields)
        self.assertIn("license_number", form.fields)
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)

    def test_form_valid_data(self):
        form_data = {
            "username": "driver1",
            "password1": "somecomplexpassword123",
            "password2": "somecomplexpassword123",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors.as_json())

    def test_form_invalid_license_number(self):
        form_data = {
            "username": "driver2",
            "password1": "somecomplexpassword123",
            "password2": "somecomplexpassword123",
            "license_number": "abc00000",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
