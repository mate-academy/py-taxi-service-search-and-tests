from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.forms import (
    CarSearchForm,
    DriverCreationForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)


class TestForms(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.form_data = {
            "username": "test_user",
            "password1": "Test123@",
            "password2": "Test123@",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "BOB11111",
        }

    def test_driver_creation_form_with_additional_fields(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, self.form_data)

    def test_driver_creation_form_with_no_license(self):
        del self.form_data["license_number"]
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_with_invalid_license(self):
        for license_number in ["bob11111", "BOB!1111", "BOB111"]:
            self.form_data["license_number"] = license_number
            form = DriverCreationForm(data=self.form_data)
            self.assertFalse(form.is_valid())

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "Test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Test")

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "Test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Test")

    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "Test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "Test")
