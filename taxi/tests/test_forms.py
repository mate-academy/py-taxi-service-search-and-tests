from django.test import TestCase
from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_with_license_number(self):
        """Test creating driver with valid license number"""
        form_data = {
            "username": "newdriver",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_license_number_validation(self):
        """Test license number format validation"""
        form_data = {
            "username": "newdriver",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "AB"  # Too short
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_license_update_form_valid(self):
        """Test updating license with valid format"""
        form_data = {"license_number": "XYZ98765"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_license_update_form_invalid(self):
        """Test updating license with invalid format"""
        form_data = {"license_number": "123"}  # Too short
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
