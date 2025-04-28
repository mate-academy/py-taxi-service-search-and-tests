from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
    validate_license_number,
)
from django.core.exceptions import ValidationError

Driver = get_user_model()


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.driver1 = Driver.objects.create_user(
            username="driver1", password="testpass1", license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2", password="testpass2", license_number="DEF67890"
        )

    def test_car_form_valid(self):
        form_data = {
            "model": "A4",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self):
        form_data = {
            "model": "",  # model is required
            "manufacturer": self.manufacturer.id,
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "newdriver",
            "password1": "Testpass123",
            "password2": "Testpass123",
            "license_number": "XYZ12345",
            "first_name": "First",
            "last_name": "Last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license(self):
        form_data = {
            "username": "newdriver",
            "password1": "Testpass123",
            "password2": "Testpass123",
            "license_number": "12345",
            "first_name": "First",
            "last_name": "Last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="testuser", password="testpass", license_number="QWE12345"
        )

    def test_driver_license_update_form_valid(self):
        form = DriverLicenseUpdateForm(
            instance=self.driver, data={"license_number": "ABC67890"}
        )
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        form = DriverLicenseUpdateForm(
            instance=self.driver, data={"license_number": "badnumber"}
        )
        self.assertFalse(form.is_valid())


class ValidateLicenseNumberTest(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_invalid_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("AB12345")

    def test_invalid_letters(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abC12345")

    def test_invalid_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC12A45")


class SearchFormsTest(TestCase):
    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "search_user"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "search_user")

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "ModelX"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "ModelX")

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "Tesla"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Tesla")
