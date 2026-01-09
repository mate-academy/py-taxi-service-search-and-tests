from django.test import TestCase
from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreationFormTests(TestCase):
    """Test driver creation form"""

    def test_driver_creation_form_valid(self):
        """Test form is valid with correct data"""
        form_data = {
            "username": "newdriver",
            "password1": "complexpass123",
            "password2": "complexpass123",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_password_mismatch(self):
        """Test form is invalid with mismatched passwords"""
        form_data = {
            "username": "newdriver",
            "password1": "complexpass123",
            "password2": "differentpass123",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTests(TestCase):
    """Test driver license update form"""

    def test_license_update_form_valid(self):
        """Test license update form with valid data"""
        form_data = {
            "license_number": "NEW12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
