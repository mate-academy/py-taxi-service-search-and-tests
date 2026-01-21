from django.test import TestCase
from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormTest(TestCase):

    def setUp(self) -> None:
        self.form_data = {
            "username": "Ser.mus",
            "first_name": "Sergii",
            "last_name": "Musienko",
            "password1": "QWER123user",
            "password2": "QWER123user",
        }

        self.wrong_license_numbers = [
            "DF12345",
            "gts12345",
            "23feA120",
            "GTE1245L",
            "TST_1234",
            "GED1234560",
        ]

        self.correct_license_numbers = [
            "QWE12345",
            "RTY67890",
            "UIO54321",
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
