from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    CarForm,
    CarSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    validate_license_number,
)
from taxi.models import Manufacturer


class FormsTests(TestCase):
    def test_validate_license_number_valid(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_validate_license_number_invalid_length(self):
        with self.assertRaises(ValidationError) as error:
            validate_license_number("ABC1234")
        self.assertEqual(
            error.exception.messages,
            ["License number should consist of 8 characters"],
        )

        with self.assertRaises(ValidationError) as error:
            validate_license_number("ABC123456")
        self.assertEqual(
            error.exception.messages,
            ["License number should consist of 8 characters"],
        )

    def test_validate_license_number_first_3_chars_not_uppercase(self):
        invalid_first_3 = ["abc12345", "12A12345", "AB112345", "A_C12345"]
        for license_num in invalid_first_3:
            with self.subTest(license_num=license_num):
                with self.assertRaises(ValidationError) as error:
                    validate_license_number(license_num)
                self.assertEqual(
                    error.exception.messages,
                    ["First 3 characters should be uppercase letters"],
                )

    def test_validate_license_number_last_5_chars_not_digits(self):
        invalid_last_5 = ["ABC1234a", "ABC1234-", "ABC1234A", "ABC123ab"]
        for license_num in invalid_last_5:
            with self.subTest(license_num=license_num):
                with self.assertRaises(ValidationError) as error:
                    validate_license_number(license_num)
                self.assertEqual(
                    error.exception.messages,
                    ["Last 5 characters should be digits"],
                )

    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "newdriver",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license(self):
        form_data = {
            "username": "newdriver",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "invalid",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_valid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "XYZ98765"})
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "xyz98765"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_car_form(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )
        driver = get_user_model().objects.create_user(
            username="testdriver2",
            password="testpassword123",
            license_number="HND12345",
        )
        form_data = {
            "model": "Civic",
            "manufacturer": manufacturer.pk,
            "drivers": [driver.pk],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "Toyo"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Toyo")

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "Cam"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Cam")

    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "driver"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "driver")
