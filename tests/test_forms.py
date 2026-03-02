from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.core.exceptions import ValidationError

from taxi.forms import (validate_license_number,
                        DriverCreationForm,
                        DriverLicenseUpdateForm,
                        DriversSearchForm,
                        CarSearchForm,
                        ManufacturerSearchForm,
                        CarForm)
from taxi.models import Manufacturer

User = get_user_model()

class LicenseValidationTests(TestCase):
    def test_valid_license(self):
        valid_license = "ABC12345"
        result = validate_license_number(valid_license)
        self.assertEqual(result, valid_license)

    def test_invalid_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234")  # 7 chars

    def test_first_three_not_uppercase(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

    def test_first_three_not_letters(self):
        with self.assertRaises(ValidationError):
            validate_license_number("12312345")

    def test_last_five_not_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC12AAA")


class DriverCreationFormTests(TestCase):
    def test_valid_form(self):
        form_data = {
            "username": "driver1",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "AAA12345",
            "first_name": "John",
            "last_name": "Doe",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_invalid_license_number(self):
        form_data = {
            "username": "driver1",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "BAD",
            "first_name": "John",
            "last_name": "Doe",
        }

        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def test_valid_update(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "BBB12345"}
        )

        self.assertTrue(form.is_valid())

    def test_invalid_update(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "123"}
        )

        self.assertFalse(form.is_valid())


class CarFormTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        self.driver = User.objects.create_user(
            username="driver1",
            password="test12345",
            license_number="AAA12345"
        )

    def test_valid_car_form(self):
        form_data = {
            "model": "Corolla",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id],  # 🔥 передаємо driver
        }

        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())


class SearchFormsTests(TestCase):
    def test_driver_search_not_required(self):
        form = DriversSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_car_search_placeholder(self):
        form = CarSearchForm()
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            "Search by model"
        )

    def test_manufacturer_search_not_required(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())


