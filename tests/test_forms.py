from django.test import TestCase
from django import forms

from django.contrib.auth import get_user_model

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Manufacturer

DRIVER = get_user_model()
USERNAME = "username"
PASSWORD = "StrongPass123!"

INVALID_LICENSE_NUMBERS = [
    "ABC1234",
    "ABC123456",
    "",
    "A1C12345",
    "abc12345",
    "AbC12345",
    "AB112345",
    "A_C12345",
    "AB-12345",
    "ABC12A45",
    "ABC1234A",
    "ABC123 5",
]


class CarFormTests(TestCase):
    def test_car_creation(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        drivers = [
            DRIVER.objects.create_user(
                username=USERNAME + str(i),
                password=PASSWORD,
                license_number="ABC1234" + str(i),
            ).id
            for i in range(3)
        ]
        form_data = {
            "model": "test_car",
            "manufacturer": manufacturer.id,
            "drivers": drivers
        }
        form = CarForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_form_contains_drivers_field(self):
        form = CarForm()
        self.assertIsInstance(
            form.fields["drivers"].widget,
            forms.CheckboxSelectMultiple
        )


class DriverCreationFormTests(TestCase):
    def test_form_contains_license_number_field(self):
        driver_creation_form = DriverCreationForm()
        self.assertIn("license_number", driver_creation_form.fields)

    def test_form_contains_last_name_field(self):
        driver_creation_form = DriverCreationForm()
        self.assertIn("last_name", driver_creation_form.fields)

    def test_form_contains_first_name_field(self):
        driver_creation_form = DriverCreationForm()
        self.assertIn("first_name", driver_creation_form.fields)

    def test_license_number_invalid(self):
        for license_number in INVALID_LICENSE_NUMBERS:
            form = DriverCreationForm({
                "username": USERNAME,
                "password1": PASSWORD,
                "password2": PASSWORD,
                "license_number": license_number,
            })
            self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTests(TestCase):
    def test_form_contains_license_number_field(self):
        driver_license_update_form = DriverLicenseUpdateForm()
        self.assertIn("license_number", driver_license_update_form.fields)

    def test_license_number_invalid(self):
        for license_number in INVALID_LICENSE_NUMBERS:
            form = DriverLicenseUpdateForm({
                "license_number": license_number,
            })
            self.assertFalse(form.is_valid())


class SearchFormsTests(TestCase):
    def test_driver_search_form_contains_username_field(self):
        driver_search_form = DriverSearchForm()
        self.assertIn("username", driver_search_form.fields)

    def test_car_search_form_contains_model_field(self):
        car_search_form = CarSearchForm()
        self.assertIn("model", car_search_form.fields)

    def test_manufacturer_search_form_contains_name_field(self):
        manufacturer_search_form = ManufacturerSearchForm()
        self.assertIn("name", manufacturer_search_form.fields)
