from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, CarForm, validate_license_number
from taxi.models import Manufacturer, Car


class FormsTests(TestCase):
    def test_driver_creation_form_license_number_first_name_last_name(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "AVF11111",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="password123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "AVF11111",
        }
        response = self.client.post(
            reverse("taxi:driver-create"), data=form_data
        )
        self.assertEqual(response.status_code, 302)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_driver_creation_form_invalid_license_number(self):
        form_data = {
            "username": "new_driver",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "license_number": "INVALID_LICENSE",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )

        self.driver1 = get_user_model().objects.create_user(
            username="driver1", password="password1", license_number="ABC123"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2", password="password2", license_number="XYZ456"
        )

    def test_car_form_valid(self):
        form_data = {
            "model": "Test Car",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid_without_drivers(self):
        form_data = {
            "model": "Test Car",
            "manufacturer": self.manufacturer.id,
            "drivers": [],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("drivers", form.errors)

    def test_car_form_invalid_without_required_fields(self):
        form_data = {
            "drivers": [self.driver1.id],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)
        self.assertIn("manufacturer", form.errors)

    def test_car_form_invalid_with_nonexistent_manufacturer(self):
        form_data = {
            "model": "Test Car",
            "manufacturer": 9999,
            "drivers": [self.driver1.id],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("manufacturer", form.errors)


class LicenseNumberValidationTest(TestCase):
    def test_valid_license_number(self):
        try:
            result = validate_license_number("ABC12345")
            self.assertEqual(result, "ABC12345")
        except ValidationError:
            self.fail(
                "validate_license_number raised ValidationError unexpectedly!"
            )

    def test_invalid_length_license_number(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("AB12345")
        self.assertEqual(
            context.exception.message,
            "License number should consist of 8 characters"
        )

        with self.assertRaises(ValidationError) as context:
            validate_license_number("ABCDEFGHI")
        self.assertEqual(
            context.exception.message,
            "License number should consist of 8 characters"
        )

    def test_invalid_first_three_characters(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("abC12345")
        self.assertEqual(
            context.exception.message,
            "First 3 characters should be uppercase letters"
        )

        with self.assertRaises(ValidationError) as context:
            validate_license_number("12312345")
        self.assertEqual(
            context.exception.message,
            "First 3 characters should be uppercase letters"
        )

    def test_invalid_last_five_characters(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("ABC12A45")
        self.assertEqual(
            context.exception.message,
            "Last 5 characters should be digits"
        )

        with self.assertRaises(ValidationError) as context:
            validate_license_number("ABC1234A")
        self.assertEqual(
            context.exception.message,
            "Last 5 characters should be digits"
        )
