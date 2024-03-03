from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)


class DriverFormsTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "test_user",
            "password1": "TestPassword123",
            "password2": "TestPassword123",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": ""
        }

    def test_creation_form_valid(self):
        self.form_data["license_number"] = "ERR45678"
        form = DriverCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, self.form_data)

    def test_invalid_form_with_lower_case(self):
        self.form_data["license_number"] = "ERr12345"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())

    def test_invalid_form_with_number_in_first_three_characters(self):
        self.form_data["license_number"] = "ER012345"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())

    def test_invalid_form_with_more_than_eight_characters(self):
        self.form_data["license_number"] = "ERR1234567"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())

    def test_invalid_form_with_less_than_eight_characters(self):
        self.form_data["license_number"] = "ERR1234"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "Test Manufacturer"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Test Manufacturer")

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "Test Model"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Test Model")

    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "test_user"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test_user")
