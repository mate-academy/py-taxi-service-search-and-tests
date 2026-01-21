from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    validate_license_number,
    DriverLicenseUpdateForm,
    CarForm, DriverSearchForm, CarSearchForm, ManufacturerSearchForm
)
from taxi.models import Manufacturer


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name(self):
        form_data = {
            "username": "testdriver",
            "password1": "test4321",
            "password2": "test4321",
            "license_number": "ASD12345",
            "first_name": "Test First",
            "last_name": "Test Last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"]
        )


class LicenseNumberValidationTests(TestCase):
    def test_valid_license_numbers(self):
        valid_numbers = ["ABC12345", "XYZ67890"]
        for number in valid_numbers:
            try:
                result = validate_license_number(number)
                self.assertEqual(result, number)
            except ValidationError:
                self.fail(
                    f"ValidationError unexpectedly raised for '{number}'"
                )

    def test_invalid_license_numbers(self):
        invalid_numbers = [
            "ABC1234",     # too short
            "abc12345",    # lowercase letters
            "AB123456",    # only 2 letters
            "ABCDE123",    # too many letters
            "ABC12A45",    # letters in digit part
            "12345678",    # no letters
        ]
        for number in invalid_numbers:
            with self.assertRaises(
                    ValidationError,
                    msg=f"Expected ValidationError for '{number}'"
            ):
                validate_license_number(number)


class DriverLicenseUpdateFormTests(TestCase):
    def test_valid_license_update(self):
        form = DriverLicenseUpdateForm(data={"license_number": "XYZ12345"})
        self.assertTrue(form.is_valid())

    def test_invalid_license_update(self):
        form = DriverLicenseUpdateForm(data={"license_number": "abc123"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_missing_license_number(self):
        form = DriverLicenseUpdateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class CarFormTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="d1",
            password="pass",
            license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="d2",
            password="pass",
            license_number="XYZ67890"
        )

    def test_car_form_valid_with_multiple_drivers(self):
        form_data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_missing_model(self):
        form_data = {
            "model": "",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)


class SearchFormTests(TestCase):
    def test_manufacturer_search_valid(self):
        form = ManufacturerSearchForm(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_empty_is_valid(self):
        form = ManufacturerSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_too_long(self):
        form = ManufacturerSearchForm(data={"name": "x" * 300})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_car_search_valid(self):
        form = CarSearchForm(data={"model": "Corolla"})
        self.assertTrue(form.is_valid())

    def test_driver_search_valid(self):
        form = DriverSearchForm(data={"username": "driver1"})
        self.assertTrue(form.is_valid())
