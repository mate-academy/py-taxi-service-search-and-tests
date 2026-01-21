from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormTest(TestCase):

    def setUp(self) -> None:
        self.form_data = {
            "username": "Bob.driver",
            "first_name": "Bobby",
            "last_name": "Lanes",
            "password1": "Test123user",
            "password2": "Test123user",
        }

        self.wrong_license_numbers = [
            "DF12345",
            "gts12345",
            "23feA120",
            "GTE1245L",
            "TSTk1242",
            "GED1234560",
        ]

        self.correct_license_numbers = [
            "TST12345",
            "WEN54321",
            "QMP00000",
        ]

    def test_create_driver_with_wrong_license_number(self) -> None:
        for license_number in self.wrong_license_numbers:
            with self.subTest(license_number):
                self.form_data["license_number"] = license_number
                form = DriverCreationForm(data=self.form_data)
                self.assertFalse(form.is_valid())

    def test_create_driver_with_correct_license_number(self) -> None:
        for license_number in self.correct_license_numbers:
            with self.subTest(license_number):
                self.form_data["license_number"] = license_number
                form = DriverCreationForm(data=self.form_data)
                self.assertTrue(form.is_valid())

    def test_update_driver_with_wrong_license_number(self) -> None:
        update_form_data = {
            "license_number": "",
        }
        for license_number in self.wrong_license_numbers:
            with self.subTest(license_number):
                update_form_data["license_number"] = license_number
                form = DriverLicenseUpdateForm(data=update_form_data)
                self.assertFalse(form.is_valid())

    def test_update_driver_with_correct_license_number(self) -> None:
        update_form_data = {
            "license_number": "",
        }
        for license_number in self.correct_license_numbers:
            with self.subTest(license_number):
                update_form_data["license_number"] = license_number
                form = DriverLicenseUpdateForm(data=update_form_data)
                self.assertTrue(form.is_valid())
