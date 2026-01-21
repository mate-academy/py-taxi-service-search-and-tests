from django.test import TestCase

from taxi.forms import (
    DriverSearchForm,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverCreationForm
)


class DriverCreationFormTests(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "TestUser",
            "password1": "password555a",
            "password2": "password555a",
            "license_number": "AAA55555",
            "first_name": "Test",
            "last_name": "Test",
        }

    def test_driver_creation_form_with_valid_data(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_creation_form_with_license_number_more_than_8_chars(self):
        self.form_data["license_number"] = "AAA555555"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_with_license_first_3_chars_not_uppercase(
            self,
    ):
        self.form_data["license_number"] = "abc12345"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_with_license_number_last_5_chars_not_digits(
            self,
    ):
        self.form_data["license_number"] = "AAA5555A"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_with_invalid_license_number(self):
        self.form_data["license_number"] = "55AAAA"


class FormsTests(TestCase):
    def test_manufacturer_search_form_is_valid(self):
        form_data = {"name": "test_manufacturer"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_form_is_valid(self):
        form_data = {"username": "test_user"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_search_form_is_valid(self):
        form_data = {"model": "test_model"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
