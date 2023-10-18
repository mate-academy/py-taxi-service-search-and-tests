from django.test import TestCase

from taxi.forms import (
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
)


class SearchFormTests(TestCase):
    def test_car_search_form_is_valid(self):
        form_data = {"model": "chifferiferrari"}

        form = CarSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "chifferiferrari")

    def test_driver_form_is_valid(self):
        form_data = {"username": "permanganates"}

        form = DriverSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "permanganates")

    def test_manufacturer_form_is_valid(self):
        form_data = {"name": "Pasta"}

        form = ManufacturerSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Pasta")


class FormTests(TestCase):
    def test_car_form_is_valid(self):
        form_data = {
            "model": "chifferiferrari",
            "manufacturer": "Ferrari",
        }

        form = CarSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "chifferiferrari")

    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "permanganates",
            "license_number": "AAA12345",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "Qfd123***",
            "password2": "Qfd123***",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_form_not_valid_if_length_less_than_8(
        self,
    ):
        form_data = {"license_number": "AAA1234"}

        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "license_number": [
                    "License number should consist of 8 characters"
                ]
            },
        )

    def test_license_form_valid_if_length_longer_than_8(
        self,
    ):
        form_data = {"license_number": "AAA1234567"}

        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "license_number": [
                    "License number should consist of 8 characters"
                ]
            },
        )

    def test_license_form_not_valid_if_first_3_chars_not_uppercase(
        self,
    ):
        form_data = {"license_number": "AaA12345"}

        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "license_number": [
                    "First 3 characters should be uppercase letters"
                ]
            },
        )

    def test_license_form_valid_if_last_5_chars_not_digits(
        self,
    ):
        form_data = {"license_number": "AAAaaaa5"}

        form = DriverLicenseUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {"license_number": ["Last 5 characters should be digits"]},
        )

    def test_license_form_valid_if_number_valid(
        self,
    ):
        form_data = {"license_number": "AAA12345"}

        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
