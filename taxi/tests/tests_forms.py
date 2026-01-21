from unittest.mock import patch
from django.test import TestCase

from django.contrib.auth import get_user_model
from taxi.models import Manufacturer
from taxi.forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm


User = get_user_model()


class CarFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="TestBrand", country="TestCountry"
        )
        cls.driver1 = User.objects.create_user(
            username="driver1", password="pass123", license_number="ASD12345"
        )
        cls.driver2 = User.objects.create_user(
            username="driver2", password="pass123", license_number="ZXC54321"
        )

    def test_form_fields(self):
        form = CarForm()
        self.assertIn("drivers", form.fields)
        self.assertEqual(
            form.fields["drivers"].__class__.__name__,
            "ModelMultipleChoiceField",
        )
        self.assertEqual(
            form.fields["drivers"].widget.__class__.__name__,
            "CheckboxSelectMultiple",
        )
        self.assertEqual(
            list(form.fields["drivers"].queryset.all()),
            list(User.objects.all()),
        )

    def test_form_valid_data(self):
        data = {
            "model": "TestModel",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_drivers(self):
        data = {
            "model": "TestModel",
            "manufacturer": self.manufacturer.id,
            "drivers": [999],
        }
        form = CarForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("drivers", form.errors)


class DriverCreationFormTest(TestCase):

    def test_form_valid_with_full_name(self):
        data = {
            "username": "Test123",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "license_number": "ASD12345",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
        }
        form = DriverCreationForm(data)
        self.assertTrue(form.is_valid())

    def test_form_without_name(self):
        data = {
            "username": "Test123",
            "license_number": "ASD12345",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
        }
        form = DriverCreationForm(data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_username(self):
        data = {
            "license_number": "ASD12345",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
        }
        form = DriverCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_form_invalid_without_password1(self):
        data = {
            "username": "Test123",
            "license_number": "ASD12345",
            "password2": "1qazcde3",
        }
        form = DriverCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)

    def test_form_invalid_without_password2(self):
        data = {
            "username": "Test123",
            "license_number": "ASD12345",
            "password1": "1qazcde3",
        }
        form = DriverCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_invalid_without_license_number(self):
        data = {
            "username": "Test123",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
        }
        form = DriverCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_form_invalid_without_username_and_password2(self):
        data = {
            "license_number": "ASD12345",
            "password1": "1qazcde3",
        }
        form = DriverCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password2", form.errors)

    def test_form_invalid_without_any_data(self):
        data = {}
        form = DriverCreationForm(data)
        expected_errors = (
            "username",
            "password1",
            "password2",
            "license_number",
        )
        self.assertFalse(form.is_valid())
        for field in expected_errors:
            self.assertIn(field, form.errors)

    @patch("taxi.forms.validate_license_number")
    def test_form_calls_license_validator(self, mock_validator):
        mock_validator.return_value = "ASD12345"

        data = {
            "username": "TestUser",
            "license_number": "ASD12345",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
        }
        form = DriverCreationForm(data)
        form.is_valid()

        mock_validator.assert_called_once_with("ASD12345")


class DriverLicenseUpdateFormTest(TestCase):

    @patch("taxi.forms.validate_license_number")
    def test_form_calls_license_validator(self, mock_validator):
        mock_validator.return_value = "ASD12345"

        data = {"license_number": "ASD12345"}
        form = DriverLicenseUpdateForm(data)
        form.is_valid()

        mock_validator.assert_called_once_with("ASD12345")
