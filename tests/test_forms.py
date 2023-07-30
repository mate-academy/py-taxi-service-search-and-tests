from django.test import TestCase

from taxi.models import Driver
from taxi.forms import DriverLicenseUpdateForm


class DriverLicenseUpdateFormTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="test_driver",
            first_name="John",
            last_name="Doe",
            email="test@site.com",
            password="password1234",
            license_number="ABC12345",
        )

    def test_valid_license_number(self):
        form_data = {"license_number": "ABC12346"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_same_number(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_length(self):
        form_data = {"license_number": "ABC12"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_uppercase(self):
        form_data = {"license_number": "abc12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_digits(self):
        form_data = {"license_number": "ABC12XYZ"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_combination(self):
        form_data = {"license_number": "abc123XYZ"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
