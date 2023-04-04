from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm,
    DriverLicenseUpdateForm
)


class DriverCreateFormTests(TestCase):
    def test_driver_create(self):
        data = {
            "username": "test1",
            "password1": "test234567",
            "password2": "test234567",
            "license_number": "AAA12345",
            "first_name": "test3",
            "last_name": "test4",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)


class DriverLicenseUpdateFormTestCase(TestCase):
    def test_valid_license_number(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["license_number"], "ABC12345")

    def test_invalid_license_number_length(self):
        form_data = {"license_number": "ABC123"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "License number should consist of 8 characters",
            form.errors["license_number"]
        )

    def test_invalid_license_number_first_three_chars_not_uppercase(self):
        form_data = {"license_number": "abc12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "First 3 characters should be uppercase letters",
            form.errors["license_number"]
        )

    def test_invalid_license_number_last_five_chars_not_digits(self):
        form_data = {"license_number": "ABC1X345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Last 5 characters should be digits",
            form.errors["license_number"]
        )


class ManufacturerSearchFormTest(TestCase):
    def test_search_by_name(self):
        form_data = {"name": "Honda"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Honda")


class CarSearchFormTest(TestCase):
    def test_search_by_model(self):
        form_data = {"model": "Accord"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Accord")


class DriverSearchFormTest(TestCase):
    def test_search_by_username(self):
        form_data = {"username": "test"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test")
