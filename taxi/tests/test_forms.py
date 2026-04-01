from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    CarModelSearchForm,
    DriverUsernameSearchForm,
    ManufacturerNameSearchForm,
)
from taxi.models import Manufacturer, Driver, Car
from django.contrib.auth import get_user_model


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Honda", country="Japan"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="driver1", password="testpass1", license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2", password="testpass2", license_number="XYZ54321"
        )

    def test_car_form_fields(self):
        """Test that CarForm has expected fields."""
        form = CarForm()
        self.assertIn("model", form.fields)
        self.assertIn("manufacturer", form.fields)
        self.assertIn("drivers", form.fields)

    def test_car_form_valid_data(self):
        """Test CarForm with valid data."""
        form_data = {
            "model": "Civic",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid_data(self):
        """Test CarForm with missing model field."""
        form_data = {
            "model": "",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)


class DriverCreationFormTest(TestCase):
    def setUp(self):
        self.base_data = {
            "username": "driver1",
            "password1": "strongPassw0rd!",
            "password2": "strongPassw0rd!",
            "first_name": "Jan",
            "last_name": "Kowalski",
        }

    def test_valid_license_number(self):
        """Test DriverCreationForm with a valid license number."""
        form_data = self.base_data.copy()
        form_data["license_number"] = "ABC12345"
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertNotIn("license_number", form.errors)

    def test_invalid_license_number_too_short(self):
        """Test DriverCreationForm with a license number too short."""
        form_data = self.base_data.copy()
        form_data["license_number"] = "AB12345"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertIn("8 characters", form.errors["license_number"][0])

    def test_invalid_license_number_letters(self):
        """Test DriverCreationForm with non-uppercase letters in license number."""
        form_data = self.base_data.copy()
        form_data["license_number"] = "abC12345"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertIn("uppercase", form.errors["license_number"][0])

    def test_invalid_license_number_digits(self):
        """Test DriverCreationForm with last 5 characters not digits."""
        form_data = self.base_data.copy()
        form_data["license_number"] = "ABC12A45"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertIn("digits", form.errors["license_number"][0])

    def test_missing_license_number(self):
        """Test DriverCreationForm missing the license_number field."""
        form_data = self.base_data.copy()
        # Don't add license_number key at all
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

        # INSERT_YOUR_CODE


class DriverUsernameSearchFormTest(TestCase):
    def test_form_valid_with_username(self):
        form = DriverUsernameSearchForm(data={"username": "johndoe"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "johndoe")

    def test_form_valid_with_empty_username(self):
        form = DriverUsernameSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_form_valid_when_username_not_provided(self):
        form = DriverUsernameSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_form_invalid_when_username_too_long(self):
        long_string = "a" * 256
        form = DriverUsernameSearchForm(data={"username": long_string})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn(
            "Ensure this value has at most 255 characters",
            form.errors["username"][0],
        )


class ManufacturerNameSearchFormTest(TestCase):
    def test_form_valid_with_name(self):
        form = ManufacturerNameSearchForm(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Toyota")

    def test_form_valid_with_empty_name(self):
        form = ManufacturerNameSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_form_valid_when_name_not_provided(self):
        form = ManufacturerNameSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_form_invalid_when_name_too_long(self):
        long_string = "a" * 256
        form = ManufacturerNameSearchForm(data={"name": long_string})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn(
            "Ensure this value has at most 255 characters",
            form.errors["name"][0],
        )
