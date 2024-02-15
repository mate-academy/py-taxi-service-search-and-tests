from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )

    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "test123456",
            "password2": "test123456",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "license_number": "JOY26458",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license_number(self):
        form_data = {
            "username": "test_user",
            "password1": "test123",
            "password2": "test123",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "license_number": "invalid_license_number",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
