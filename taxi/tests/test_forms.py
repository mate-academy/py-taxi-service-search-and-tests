from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Driver


class DriverCreationFormTests(TestCase):
    def test_valid_data(self):
        form_data = {
            "username": "newdriver",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "license_number": "ABC12345",
            "first_name": "New",
            "last_name": "Driver",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        driver = form.save()
        self.assertEqual(driver.username, "newdriver")
        self.assertEqual(driver.license_number, "ABC12345")

    def test_invalid_license_number(self):
        form_data = {
            "username": "newdriver",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "license_number": "INVALID",
            "first_name": "New",
            "last_name": "Driver",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"],
        )


class DriverLicenseUpdateFormTests(TestCase):
    def test_valid_license_number_update(self):
        driver = Driver.objects.create_user(
            username="existingdriver",
            password="password123",
            license_number="XYZ67890"
        )
        form_data = {"license_number": "DEF54321"}
        form = DriverLicenseUpdateForm(data=form_data, instance=driver)
        self.assertTrue(form.is_valid())
        updated_driver = form.save()
        self.assertEqual(updated_driver.license_number, "DEF54321")

    def test_invalid_license_number_update(self):
        driver = Driver.objects.create_user(
            username="existingdriver",
            password="password123",
            license_number="XYZ67890"
        )
        form_data = {"license_number": "BADNUM"}
        form = DriverLicenseUpdateForm(data=form_data, instance=driver)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"],
        )
