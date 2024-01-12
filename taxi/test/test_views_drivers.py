from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, validate_license_number
from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="12345ps.",
        )
        self.client.force_login(self.user)

    def test_driver_creation_form_clean_license_number(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "license_number": "ABC12346",
            "first_name": "Test",
            "last_name": "User",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        cleaned_license_number = form.clean_license_number()
        self.assertEqual(cleaned_license_number, "ABC12346")

    def test_validate_license_number(self):
        valid_license_number = "ABC12345"
        invalid_license_number = "invalid_license"
        self.assertEqual(
            validate_license_number(valid_license_number), valid_license_number
        )
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)
