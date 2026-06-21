from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        CarModelSearchForm,
                        ManufacturerNameSearchForm,
                        DriverUsernameSearchForm)


class TestForms(TestCase):
    def test_driver_creation_from_valid_license(self):
        form_data = {
            "username": "NewDriver",
            "password1": "Secr3t_Pa55w0rd!",
            "password2": "Secr3t_Pa55w0rd!",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_license_number_wrong_length(self):
        form_data = {
            "license_number": "ABC1234",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"][0],
            "License number should consist of 8 characters",
        )

    def test_license_number_first_3_not_uppercase_letters(self):
        form_data = {
            "license_number": "AbC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"][0],
            "First 3 characters should be uppercase letters",
        )

    def test_license_number_last_5_not_digits(self):
        form_data = {
            "license_number": "ABC123d5",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertEqual(
            form.errors["license_number"][0],
            "Last 5 characters should be digits"
        )

    def test_car_model_search_form_can_be_empty(self):
        form_data = {"model": ""}
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_name_search_form_can_be_empty(self):
        form_data = {"name": ""}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_username_search_form_can_be_empty(self):
        form_data = {"username": ""}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
