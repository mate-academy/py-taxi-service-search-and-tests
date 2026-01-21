from django.test import TestCase

from django.contrib.auth import get_user_model

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class TestDriverForm(TestCase):
    LICENSES = ["A", "asdweawes", "Aaa12345", "AAA1234k"]

    def test_driver_license_creation_validation(self):
        for license_ in self.LICENSES:
            with self.subTest(license=license_):
                form_data = {
                    "username": "TestDriver",
                    "password1": "TestPassword",
                    "password2": "TestPassword",
                    "license_number": license_,
                }
                form = DriverCreationForm(data=form_data)
                self.assertFalse(form.is_valid())

    def test_update_license_validation(self):
        driver = get_user_model().objects.create_user(
            username="TestDriver",
            password="TestPassword",
            license_number="AAA12345"
        )
        for license_ in self.LICENSES:
            with self.subTest(license=license_):
                form_data = {
                    "driver": driver,
                    "license_number": license_,
                }
                form = DriverLicenseUpdateForm(data=form_data)
                self.assertFalse(form.is_valid())
