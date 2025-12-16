from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    ManufacturerSearchForm,
    CarForm,
    CarSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    validate_license_number
)
from taxi.models import Manufacturer, Car
from django.core.exceptions import ValidationError


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_form_valid(self):
        form = ManufacturerSearchForm(data={"name": "Test Manufacturer"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Test Manufacturer")

    def test_manufacturer_search_form_empty_name(self):
        form = ManufacturerSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_manufacturer_search_form_no_data(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")


class CarSearchFormTest(TestCase):
    def test_car_search_form_valid(self):
        form = CarSearchForm(data={"model": "Test Model"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Test Model")

    def test_car_search_form_empty_model(self):
        form = CarSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_car_search_form_no_data(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")


class DriverSearchFormTest(TestCase):
    def test_driver_search_form_valid(self):
        form = DriverSearchForm(data={"username": "testuser"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testuser")

    def test_driver_search_form_empty_username(self):
        form = DriverSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_driver_search_form_no_data(self):
        form = DriverSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")


class LicenseNumberValidationTest(TestCase):
    def test_validate_license_number_valid(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_validate_license_number_invalid_length(self):
        with self.assertRaisesMessage(
                ValidationError,
                "License number should consist of 8 characters"
        ):
            validate_license_number("ABC1234")
        with self.assertRaisesMessage(
                ValidationError,
                "License number should consist of 8 characters"
        ):
            validate_license_number("ABC123456")

    def test_validate_license_number_invalid_prefix_not_uppercase(self):
        with self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters"
        ):
            validate_license_number("abc12345")

    def test_validate_license_number_invalid_prefix_not_alpha(self):
        with self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters"
        ):
            validate_license_number("AB123456")

    def test_validate_license_number_invalid_suffix_not_digit(self):
        with self.assertRaisesMessage(
                ValidationError,
                "Last 5 characters should be digits"
        ):
            validate_license_number("ABCDEABC")
        with self.assertRaisesMessage(
                ValidationError,
                "Last 5 characters should be digits"
        ):
            validate_license_number("ABC1234A")


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "newdriver",
            "password1": "ValidPassword123",
            "password2": "ValidPassword123",
            "license_number": "XYZ54321",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_driver_creation_form_invalid_license_number(self):
        form_data = {
            "username": "newdriver2",
            "password1": "ValidPassword123",
            "password2": "ValidPassword123",
            "license_number": "XYZ1234",  # Invalid length
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertIn(
            "License number should consist of 8 characters",
            form.errors["license_number"]
        )

    def test_driver_creation_form_password_mismatch(self):
        form_data = {
            "username": "newdriver3",
            "password1": "ValidPassword123",
            "password2": "MismatchPassword",
            "license_number": "XYZ54322",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
        self.assertIn(
            "The two password fields didn’t match.",
            form.errors["password2"]
        )


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_valid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC98765"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_driver_license_update_form_invalid_license_number(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC123"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertIn(
            "License number should consist of 8 characters",
            form.errors["license_number"]
        )


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestMan",
            country="TestCountry"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="pwd",
            license_number="DRV11111"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="pwd",
            license_number="DRV22222"
        )

    def test_car_form_valid(self):
        form_data = {
            "model": "TestCarModel",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver1.pk, self.driver2.pk],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_car_form_missing_model(self):
        form_data = {
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver1.pk],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)
        self.assertIn("This field is required.", form.errors["model"])

    def test_car_form_missing_manufacturer(self):
        form_data = {
            "model": "TestCarModel",
            "drivers": [self.driver1.pk],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("manufacturer", form.errors)
        self.assertIn("This field is required.", form.errors["manufacturer"])

    def test_car_form_no_drivers(self):
        form_data = {
            "model": "TestCarModel",
            "manufacturer": self.manufacturer.pk,
            "drivers": [],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("drivers", form.errors)
        self.assertIn("This field is required.", form.errors["drivers"])
