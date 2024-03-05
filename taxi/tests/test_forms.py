from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm,
)


class FormsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="TestPassword345"
        )
        self.form_data = {
            "username": "test_username",
            "password1": "TestPassword1",
            "password2": "TestPassword1",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "ABC12345",
        }

    def test_driver_creation_form_with_valid_data(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_creation_with_wrong_license(self):
        wrong_license_numbers = ["1111111", "", "ABCDFET"]
        for license_number in wrong_license_numbers:
            self.form_data["license_number"] = license_number
            form = DriverCreationForm(data=self.form_data)
            self.assertFalse(form.is_valid())


class TestSearchForms(TestCase):
    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "Manufacturer"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Manufacturer")

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "Car"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Car")

    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "Driver"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "Driver")
