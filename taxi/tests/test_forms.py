from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Manufacturer
from taxi.tests.test_views.initial_data import DRIVERS_DATA


class CarFormTest(TestCase):
    def test_car_form_valid(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )

        user = get_user_model().objects.create_user(
            username="test_username",
            license_number="ABC12346",
            password="Test1234q",
        )

        form_data = {
            "model": "test_model",
            "manufacturer": manufacturer.id,
            "drivers": [user.id],
        }

        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self):
        form_data = {
            "model": "test_model",
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form = DriverCreationForm(data=DRIVERS_DATA)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid(self):
        form = DriverCreationForm(data={
            "username": "test",
        })
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_valid(self):
        form = DriverLicenseUpdateForm(data={
            "license_number": "ABC12345",
        })
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid(self):
        form = DriverLicenseUpdateForm(data={
            "license_number": "abc12345",
        })
        self.assertFalse(form.is_valid())


class ValidateLicenseNumberTest(TestCase):
    def test_valid_license_number(self):
        valid_license_number = "ABC12345"
        self.assertEqual(
            validate_license_number(valid_license_number),
            valid_license_number
        )

    def test_invalid_length(self):
        invalid_license_number = "ABC123"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_first_characters(self):
        invalid_license_number = "abc12345"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_last_characters(self):
        invalid_license_number = "ABCxyz12"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)


class DriverSearchFormTest(TestCase):
    def test_form_fields(self):
        form = DriverSearchForm()
        self.assertEqual(len(form.fields), 1)
        self.assertIn("username", form.fields)

    def test_form_valid_data(self):
        form = DriverSearchForm(data={"username": "test_username"})
        self.assertTrue(form.is_valid())

    def test_form_empty_data(self):
        form = DriverSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_form_max_length(self):
        form = DriverSearchForm()
        self.assertEqual(form.fields["username"].max_length, 255)

    def test_form_widget_attributes(self):
        form = DriverSearchForm()
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Search by username")
        self.assertEqual(
            form.fields["username"].widget.attrs["size"],
            "100")


class CarSearchFormTest(TestCase):
    def test_form_fields(self):
        form = CarSearchForm()
        self.assertEqual(len(form.fields), 1)
        self.assertIn("model", form.fields)

    def test_form_valid_data(self):
        form = CarSearchForm(data={"model": "test_model"})
        self.assertTrue(form.is_valid())

    def test_form_empty_data(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_form_max_length(self):
        form = CarSearchForm()
        self.assertEqual(form.fields["model"].max_length, 255)

    def test_form_widget_attributes(self):
        form = CarSearchForm()
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            "Search by model")
        self.assertEqual(
            form.fields["model"].widget.attrs["size"],
            "100")


class ManufacturerSearchFormTest(TestCase):
    def test_form_fields(self):
        form = ManufacturerSearchForm()
        self.assertEqual(len(form.fields), 1)
        self.assertIn("name", form.fields)

    def test_form_valid_data(self):
        form = ManufacturerSearchForm(data={"name": "test_name"})
        self.assertTrue(form.is_valid())

    def test_form_empty_data(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_form_max_length(self):
        form = ManufacturerSearchForm()
        self.assertEqual(form.fields["name"].max_length, 255)

    def test_form_widget_attributes(self):
        form = ManufacturerSearchForm()
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Search by name")
        self.assertEqual(
            form.fields["name"].widget.attrs["size"],
            "100")
