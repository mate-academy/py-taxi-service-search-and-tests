from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_driver_creating_with_additional_inf(self):
        form_data = {
            "username": "new_user",
            "password1": "user123456",
            "password2": "user123456",
            "license_number": "LIC12345",
            "first_name": "User first",
            "last_name": "User last"
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)

    def test_validation_driver_create_license_num_len(self):

        form_data = {
            "username": "test",
            "password": "test123456",
            "license_number": "LIC12345687"
        }

        form = DriverCreationForm(data=form_data)

        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"]
        )

    def test_validation_driver_create_license_num_isalpha(self):

        form_data = {
            "username": "test",
            "password": "test123456",
            "license_number": "LI112345"
        }

        form = DriverCreationForm(data=form_data)

        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"]
        )

    def test_validation_driver_create_license_num_isupper(self):

        form_data = {
            "username": "test",
            "password": "test123456",
            "license_number": "LIa12345"
        }

        form = DriverCreationForm(data=form_data)

        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"]
        )

    def test_validation_driver_create_license_num_isdigit(self):

        form_data = {
            "username": "test",
            "password": "test123456",
            "license_number": "LIC1234a"
        }

        form = DriverCreationForm(data=form_data)

        self.assertEqual(
            form.errors["license_number"],
            ["Last 5 characters should be digits"]
        )

    def test_validation_driver_update_license_num_len(self):

        form_data = {
            "license_number": "LIC12345687"
        }

        form = DriverLicenseUpdateForm(data=form_data)

        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"]
        )

    def test_validation_driver_update_license_num_isalpha(self):

        form_data = {
            "license_number": "LI112345"
        }

        form = DriverLicenseUpdateForm(data=form_data)

        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"]
        )

    def test_validation_driver_update_license_num_isupper(self):

        form_data = {
            "license_number": "LIa12345"
        }

        form = DriverLicenseUpdateForm(data=form_data)

        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"]
        )

    def test_validation_driver_update_license_num_isdigit(self):

        form_data = {
            "license_number": "LIC1234a"
        }

        form = DriverLicenseUpdateForm(data=form_data)

        self.assertEqual(
            form.errors["license_number"],
            ["Last 5 characters should be digits"]
        )
