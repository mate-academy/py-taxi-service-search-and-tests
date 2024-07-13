from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class CreateFormsTest(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "test_username",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "TST12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class UpdateFormsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="1qazcde3",
            license_number="TST12345"
        )
        self.client.force_login(self.user)

    def test_driver_license_number_update_form(self):
        form_data = {"license_number": "NEW12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"],
        )
