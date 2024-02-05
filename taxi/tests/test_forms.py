from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    DriverLicenseUpdateForm,
    DriverCreationForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)


class TestForms(TestCase):
    """
    TestCase class for testing the forms in the taxi app.
    """

    def setUp(self):
        """
        Set up necessary data for the tests.
        """
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )

    def test_driver_license_update_form_valid_data(self):
        """
        Tests the DriverLicenseUpdateForm with valid data.
        """
        form_data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_data(self):
        """
        Tests the DriverCreationForm with invalid data.
        """
        form_data = {
            "username": "New_driver",
            "password1": "new_drivers_password",
            "password2": "different_password",
            "license_number": "ABC12345",
            "first_name": "New",
            "last_name": "Driver"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_driver_license_update_form_invalid_data(self):
        """
        Tests the DriverLicenseUpdateForm with invalid data.
        """
        form_data = {
            "license_number": "InvalidLicenseNumber"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_search_form_valid_data(self):
        """
        Tests the DriverSearchForm with valid data.
        """
        form_data = {
            "username": "search_user"
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form_valid_data(self):
        """
        Tests the CarSearchForm with valid data.
        """
        form_data = {
            "model": "search_model"
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_valid_data(self):
        """
        Tests the ManufacturerSearchForm with valid data.
        """
        form_data = {
            "name": "search_manufacturer"
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
