from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarForm,
    SearchForm,
    validate_license_number,
)
from taxi.models import Manufacturer, Car
from django.core.exceptions import ValidationError


class DriverCreationFormTests(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "testuser",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "Test",
            "last_name": "User",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"],
            "ABC12345"
        )

    def test_driver_creation_form_invalid_license(self):
        form = DriverCreationForm(
            data={
                "username": "testuser",
                "password1": "1qazcde3",
                "password2": "1qazcde3",
                "first_name": "Test",
                "last_name": "User",
                "license_number": "INVALID",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def test_update_form_valid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())

    def test_update_form_invalid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "123"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class CarFormTests(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="u1", password="test123", license_number="AAA11111"
        )
        self.user2 = get_user_model().objects.create_user(
            username="u2", password="test123", license_number="BBB22222"
        )
        self.manufacturer = Manufacturer.objects.create(name="BMW",
                                                        country="DE")
        self.car = Car.objects.create(model="M3",
                                      manufacturer=self.manufacturer)

    def test_car_form_valid(self):
        form_data = {
            "model": "M3 Updated",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user1.id, self.user2.id],
        }
        form = CarForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.cleaned_data["drivers"]),
                         [self.user1, self.user2])


class SearchFormTests(TestCase):
    def test_search_form_placeholder(self):
        form = SearchForm()
        self.assertEqual(
            form.fields["search_term"].widget.attrs["placeholder"],
            "Search"
        )


class ValidateLicenseNumberTests(TestCase):
    def test_correct_license_number(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_invalid_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC123")

    def test_invalid_letters(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

    def test_invalid_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC12abc")
