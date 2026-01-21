from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverCreationFormTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "some_username",
            "password1": "some_password123",
            "password2": "some_password123",
            "license_number": "ABC12345"
        }

    def test_form_is_valid(self) -> None:
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_license_number_validation(self) -> None:
        self.form_data["license_number"] = "123"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        self.form_data["license_number"] = "ABc12345"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        self.form_data["license_number"] = "12312345"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        self.form_data["license_number"] = "ZXC12345"
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    class DriverLicenseUpdateFormTest(TestCase):
        def test_license_number_validation(self) -> None:
            form = DriverLicenseUpdateForm(data={
                "license_number": 123
            })
            self.assertFalse(form.is_valid())

            form = DriverLicenseUpdateForm(data={
                "license_number": 123
            })
            self.assertFalse(form.is_valid())

            form = DriverLicenseUpdateForm(data={
                "license_number": 123
            })
            self.assertFalse(form.is_valid())

            form = DriverLicenseUpdateForm(data={
                "license_number": 123
            })
            self.assertFalse(form.is_valid())
