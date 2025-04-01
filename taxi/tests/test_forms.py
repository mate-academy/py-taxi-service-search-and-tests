from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverLicenseUpdateForm, CustomDriverCreationForm

User = get_user_model()


class FormsTests(TestCase):
    def test_driver_creation_form_first_name_last_name_license(self):
        form_data = {
            "username": "new_user",
            "password1": "abc12Test",
            "password2": "abc12Test",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "AAV12345"
        }
        form = CustomDriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
        self.assertNotIn("license_number", form.errors)

    def test_license_number_valid(self):
        """
        Test valid license number form with validators
        """
        form_data = {
            "username": "test_user",
            "license_number": "ABC12341"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertNotIn("license_number", form.errors)

    def test_license_number_invalid(self):
        """
        Test valid license number form with validators
        """
        form_data = {
            "username": "testuser",
            "license_number": "aABC12341s"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(len(form.errors["license_number"]), 3)

    def test_create_user_with_custom_form(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="Bob",
            password="abc12Test"
        )
        self.client.force_login(self.user)

        form_data = {
            "username": "test_user",
            "password1": "abc12Test",
            "password2": "abc12Test",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "AAV12345"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = User.objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
