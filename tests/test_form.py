from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class TestDriverCreationForm(TestCase):
    def test_create_driver_with_valid_data(self):
        form_data = {
            "username": "test_driver",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "test_password12",
            "password2": "test_password12",
            "license_number": "BAC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_driver_with_lowercase_in_license(self):
        form_data = {
            "username": "test_driver",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "test_password12",
            "password2": "test_password12",
            "license_number": "bac12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_driver_without_letters_in_license(self):
        form_data = {
            "username": "test_driver",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "test_password12",
            "password2": "test_password12",
            "license_number": "32112345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_driver_with_1_symbol_in_license(self):
        form_data = {
            "username": "test_driver",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "test_password12",
            "password2": "test_password12",
            "license_number": "1",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestDriverLicenseUpdateForm(TestCase):
    def test_update_driver_license_with_valid_data(self):
        form_data = {"license_number": "BAC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_update_driver_license_with_lowercase(self):
        form_data = {"license_number": "bac12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    """without letters or with another number of symbols by analogy"""
