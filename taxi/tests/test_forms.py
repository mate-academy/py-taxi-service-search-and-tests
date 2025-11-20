from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.models import (
    Car,
    Manufacturer,
)

from taxi.forms import (
    DriverLicenseUpdateForm,
    DriverCreationForm,
    validate_license_number
)
from taxi.urls import app_name


class TestValidateLicenseNumber(TestCase):

    def test_true_value_for_license_number(self):
        self.assertTrue(validate_license_number("TES33355"))

    def test_lower_value_for_license_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("tes33355")

    def test_low_length_license_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("TES3335")

    def test_isdigit_license_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("33335555")

    def test_isalpha_license_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("TESttest")


class TestFormValidateLicenseNumber(TestCase):

    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="test-manufacturer",
            country="test-country"
        )
        user = get_user_model().objects.create_user(
            username="test-user",
            license_number="TES33355",
        )
        Car.objects.create(
            model="test-model",
            manufacturer_id=1,
        ).drivers.add(user)

    def test_driver_creation_form(self):
        data = {
            "username": "user-test",
            "license_number": "TES98555",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        form.save()

        # first user created in setUpTestData
        self.assertEqual(get_user_model().objects.count(), 2)

        form_user = get_user_model().objects.get(pk=2)
        self.assertTrue(
            form_user.username == data["username"] and
            form_user.license_number == data["license_number"]
        )
        self.assertTrue(
            form_user.check_password("1qazcde3")
        )

    def test_driver_create_used_validation(self):
        data = {
            "username": "user-test",
            "license_number": "novalid",
        }
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_driver_update_license_number(self):
        data = {
            "license_number": "TES44455",
        }
        form = DriverLicenseUpdateForm(instance=get_user_model().objects.get(pk=1), data=data)

        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(
            get_user_model().objects.get(pk=1).license_number,
            data["license_number"],
        )

    def test_driver_update_used_validation(self):
        data = {
            "license_number": "novalid",
        }
        form = DriverLicenseUpdateForm(instance=get_user_model().objects.get(pk=1), data=data)
        self.assertFalse(form.is_valid())
