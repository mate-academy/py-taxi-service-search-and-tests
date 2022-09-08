from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import validate_license_number, DriverCreationForm


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

        self.form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "AAA12345"
        }

        self.client.post(reverse("taxi:driver-create"), data=self.form_data)

    def test_driver_creation_form_with_driver_license_is_valid(self):

        driver = get_user_model().objects.get(username=self.form_data["username"])
        self.assertEqual(driver.license_number, self.form_data["license_number"])

    def test_driver_license_update_form_with_driver_license_is_valid(self):
        updated_data = {
            "license_number": "BBB11111"
        }
        driver = get_user_model().objects.get(username=self.form_data["username"])
        self.client.post(reverse("taxi:driver-update", args=(driver.id,)), data=updated_data)
        driver.refresh_from_db()
        self.assertEqual(driver.license_number, "BBB11111")


class ValidLicenseNumberTest(TestCase):
    def test_validate_license_number_correct_value(self):
        self.license_number = "UAI12345"

        self.assertEqual(
            validate_license_number(self.license_number),
            self.license_number
        )

    def test_validate_license_number_doesnt_consist_of_8_characters(self):
        self.license_number = "1234567"
        try:
            validate_license_number(self.license_number)
        except ValidationError as error:
            self.error = error

        self.assertEqual(
            self.error,
            ValidationError("License number should consist of 8 characters")
        )

    def test_validate_license_number_doesnt_have_3_first_uppercase_characters(self):
        self.license_number = "12345678"
        try:
            validate_license_number(self.license_number)
        except ValidationError as error:
            self.error = error

        self.assertEqual(
            self.error,
            ValidationError("First 3 characters should be uppercase letters")
        )

    def test_validate_license_number_doesnt_have_5_last_digit_characters(self):
        self.license_number = "UAIE1234"
        try:
            validate_license_number(self.license_number)
        except ValidationError as error:
            self.error = error

        self.assertEqual(
            self.error,
            ValidationError("Last 5 characters should be digits")
        )






