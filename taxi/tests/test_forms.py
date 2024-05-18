from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm, CarForm


class DriverCreationFormTest(TestCase):
    def test_form_fields(self):
        form = DriverCreationForm()
        self.assertIn("license_number", form.fields)
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)

    def test_form_initial_values(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="Test123",
            first_name="Test_first",
            last_name="Test_last",
            license_number="ABC12345"
        )

        form = CarForm(instance=driver)

        self.assertEqual(form.initial["username"], driver.username)
        self.assertEqual(form.initial["first_name"], driver.first_name)
        self.assertEqual(form.initial["last_name"], driver.last_name)
        self.assertEqual(form.initial["license_number"], driver.license_number)
        self.assertTrue(driver.check_password("Test123"))

    def test_form_update_driver_license_8_length(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC1234"})
        self.assertFalse(form.is_valid())

    def test_form_update_driver_license_3th_chars_upper(self):
        form = DriverLicenseUpdateForm(data={"license_number": "AsC12345"})
        self.assertFalse(form.is_valid())

    def test_form_update_driver_license_last_5_chars_digits(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABCdefgh"})
        self.assertFalse(form.is_valid())
