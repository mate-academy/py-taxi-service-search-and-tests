from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm


class TestDriverLicenseUpdateForm(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            first_name="Test",
            last_name="User",
            license_number="ABC12345",
        )

    def test_form_valid_data(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "XYZ98765"},
            instance=self.user
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["license_number"], "XYZ98765")

    def test_form_invalid_license_number(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "123456789"},
            instance=self.user
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
