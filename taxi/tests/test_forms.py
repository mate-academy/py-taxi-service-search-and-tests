from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreationFormTest(TestCase):

    def setUp(self) -> None:
        self.driver_correct_data = {
            "username": "test_driver",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "ADM56984",
            "first_name": "fist_name",
            "last_name": "last_name"
        }

    def test_create_driver_with_correct_data(self) -> None:
        driver = DriverCreationForm(self.driver_correct_data)
        self.assertTrue(driver.is_valid())

    def test_crete_driver_with_incorrect_license(self) -> None:
        self.driver_correct_data["license_number"] = "ADM5698"
        driver = DriverCreationForm(self.driver_correct_data)
        self.assertFalse(driver.is_valid())


class DriverLicenseUpdateFormTest(TestCase):

    def test_with_correct_new_license(self) -> None:
        license_ = DriverLicenseUpdateForm({"license_number": "BDM56984"})
        self.assertTrue(license_.is_valid())

    def test_with_incorrect_nwe_license(self) -> None:
        license_ = DriverLicenseUpdateForm({"license_number": "zDM56984"})
        self.assertFalse(license_.is_valid())
