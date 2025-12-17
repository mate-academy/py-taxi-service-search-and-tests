from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarForm,
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    validate_license_number,
)
from taxi.models import Manufacturer


class LicenceValidationFormTest(TestCase):
    def test_valid_license(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_license_too_short(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC123")

    def test_license_too_long(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC123456")

    def test_license_not_upper(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

    def test_license_not_digits_at_end(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC12A45")


class DriverCreationFormTest(TestCase):
    def test_create_driver_valid_data(self):
        form_data = {
            "username": "driver_test",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
            "first_name": "Bob",
            "last_name": "Bobovich",
            "license_number": "AAA11111",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_invalid_licence(self):
        form_data = {
            "username": "driver_test",
            "password1": "Password123",
            "password2": "Password123",
            "license_number": "invalid",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(TestCase):
    def test_update_licence_valid(self):
        form_data = {"license_number": "BBB55555"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_update_license_invalid(self):
        form_data = {"license_number": "bBb222"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"][0],
            "License number should consist of 8 characters"
        )


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="d1", password="p1", license_number="AAA00001"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="d2", password="p2", license_number="AAA00002"
        )

    def test_car_valid(self):
        form_data = {
            "model": "A6",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        car = form.save()
        self.assertEqual(car.drivers.count(), 2)


class SearchFormTest(TestCase):
    def test_car_search_form_empty(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_driver_search_form_valid(self):
        form = DriverSearchForm(data={"username": "test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test")

    def test_manufacturer_search_form_empty(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")
