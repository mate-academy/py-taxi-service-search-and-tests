from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriversSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)


class DriverCreationFormTests(TestCase):
    def test_driver_creation_form_with_valid_license_number(self):
        form_data = {
            "username": "test_driver",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_driver_creation_form_with_invalid_license_number_length(self):
        form_data = {
            "username": "test_driver",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
            "license_number": "ABC1234",
            "first_name": "John",
            "last_name": "Doe",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_with_lowercase_first_three_chars(self):
        form_data = {
            "username": "test_driver",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
            "license_number": "abc12345",
            "first_name": "John",
            "last_name": "Doe",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_with_non_digit_last_five_chars(self):
        form_data = {
            "username": "test_driver",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
            "license_number": "ABC12A45",
            "first_name": "John",
            "last_name": "Doe",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def test_license_update_form_with_valid_license_number(self):
        form = DriverLicenseUpdateForm(data={
            "license_number": "XYZ98765"
        })

        self.assertTrue(form.is_valid())

    def test_license_update_form_with_invalid_license_number(self):
        form = DriverLicenseUpdateForm(data={
            "license_number": "xyz98765"
        })

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class SearchFormsTests(TestCase):
    def test_drivers_search_form_with_empty_data_is_valid(self):
        form = DriversSearchForm(data={"username": ""})

        self.assertTrue(form.is_valid())

    def test_drivers_search_form_with_username_is_valid(self):
        form = DriversSearchForm(data={"username": "john"})

        self.assertTrue(form.is_valid())

    def test_car_search_form_with_empty_data_is_valid(self):
        form = CarSearchForm(data={"model": ""})

        self.assertTrue(form.is_valid())

    def test_car_search_form_with_model_is_valid(self):
        form = CarSearchForm(data={"model": "X5"})

        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_with_empty_data_is_valid(self):
        form = ManufacturerSearchForm(data={"name": ""})

        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_with_name_is_valid(self):
        form = ManufacturerSearchForm(data={"name": "Toyota"})

        self.assertTrue(form.is_valid())
