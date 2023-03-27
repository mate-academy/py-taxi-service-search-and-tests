from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreationFormTest(TestCase):
    def test_driver_creation_valid_form(self):
        form_data = {
            "username": "testuser",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "User",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_invalid_form(self):
        form_data = {
            "username": "testuser",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "ABCD1234",
            "first_name": "",
            "last_name": "",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_valid_form(self):
        driver = get_user_model().objects.create(username="testdriver")
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC12345"},
            instance=driver
        )
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        driver = get_user_model().objects.create(username="testdriver")
        form = DriverLicenseUpdateForm(
            data={"license_number": "aBc12345"},
            instance=driver
        )
        self.assertFalse(form.is_valid())
