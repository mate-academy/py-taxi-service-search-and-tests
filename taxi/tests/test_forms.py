from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)


class FormTests(TestCase):
    def setUp(self):
        self.create_data = {
            "username": "test",
            "password1": "tesT123jh",
            "password2": "tesT123jh",
            "first_name": "first_test",
            "last_name": "last_test",
            "license_number": "AMD12345"
        }

        self.update_data = {
            "license_number": "AMD12345"
        }

    def test_driver_creation_form_with_first_last_name_and_license_number(
            self
    ):
        form = DriverCreationForm(data=self.create_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.create_data)

    def test_validate_license_number_with_length_not_equal_8(self):
        self.create_data["license_number"] = "AMD1234"
        create_form = DriverCreationForm(data=self.create_data)
        self.assertFalse(create_form.is_valid())

        self.update_data["license_number"] = "AMD1234"
        update_form = DriverLicenseUpdateForm(data=self.update_data)
        self.assertFalse(update_form.is_valid())

    def test_validate_license_number_with_first_3_characters_not_uppercase(
            self
    ):
        self.create_data["license_number"] = "amD12345"
        create_form = DriverCreationForm(data=self.create_data)
        self.assertFalse(create_form.is_valid())

        self.update_data["license_number"] = "amD12345"
        update_form = DriverLicenseUpdateForm(data=self.update_data)
        self.assertFalse(update_form.is_valid())

    def test_validate_license_number_with_last_5_characters_not_digits(self):
        self.create_data["license_number"] = "AMD1234a"
        create_form = DriverCreationForm(data=self.create_data)
        self.assertFalse(create_form.is_valid())

        self.update_data["license_number"] = "AMD1234a"
        update_form = DriverLicenseUpdateForm(data=self.update_data)
        self.assertFalse(update_form.is_valid())

    def test_driver_search_form(self):
        not_empty_form = DriverSearchForm(data={"username": "test"})
        empty_form = DriverSearchForm(data={"username": ""})

        self.assertTrue(not_empty_form.is_valid())
        self.assertTrue(empty_form.is_valid())
        self.assertEqual(not_empty_form.cleaned_data["username"], "test")
        self.assertEqual(empty_form.cleaned_data["username"], "")

    def test_car_search_form(self):
        not_empty_form = CarSearchForm(data={"model": "test"})
        empty_form = CarSearchForm(data={"model": ""})

        self.assertTrue(not_empty_form.is_valid())
        self.assertTrue(empty_form.is_valid())
        self.assertEqual(not_empty_form.cleaned_data["model"], "test")
        self.assertEqual(empty_form.cleaned_data["model"], "")

    def test_manufacturer_search_form(self):
        not_empty_form = ManufacturerSearchForm(data={"name": "test"})
        empty_form = ManufacturerSearchForm(data={"name": ""})

        self.assertTrue(not_empty_form.is_valid())
        self.assertTrue(empty_form.is_valid())
        self.assertEqual(not_empty_form.cleaned_data["name"], "test")
        self.assertEqual(empty_form.cleaned_data["name"], "")
