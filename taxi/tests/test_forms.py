from django.test import TestCase
from taxi.models import Driver
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number,
)


class DriverFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create_user(
            username="user1",
            password="Str0ng-Passw0rd!",
            license_number="RFC34532"
        )

    def test_validate_license_number_len_equal_8(self):
        license_d = self.driver.license_number
        self.assertEqual(len(license_d), 8)

    def test_license_number_first_3_letters_are_upper_and_alpha(self):
        first_3 = self.driver.license_number[:3]
        self.assertTrue(first_3.isupper() and first_3.isalpha())

    def test_license_number_last_5_letters_are_digits(self):
        last_5 = self.driver.license_number[3:]
        self.assertTrue(last_5.isdigit())


User = get_user_model()


class DriverCreationFormTest(TestCase):
    def test_valid_data_creates_user(self):
        form = DriverCreationForm(
            data={
                "username": "u1",
                "password1": "Str0ng-Pa55!",
                "password2": "Str0ng-Pa55!",
                "first_name": "Neo",
                "last_name": "Driver",
                "license_number": "ABC12345",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertTrue(User.objects.filter(
            pk=user.pk,
            license_number="ABC12345"
        ).exists())

    def test_invalid_license_length(self):
        form = DriverCreationForm(
            data={
                "username": "u2",
                "password1": "Str0ng-Pa55!",
                "password2": "Str0ng-Pa55!",
                "first_name": "Neo",
                "last_name": "Driver",
                "license_number": "AB1234",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("License number "
                      "should consist of 8 "
                      "characters",
                      form.errors["license_number"])

    def test_invalid_license_not_uppercase(self):
        form = DriverCreationForm(
            data={
                "username": "u3",
                "password1": "Str0ng-Pa55!",
                "password2": "Str0ng-Pa55!",
                "first_name": "Neo",
                "last_name": "Driver",
                "license_number": "abC12345",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "First 3 characters should "
            "be uppercase letters",
            form.errors["license_number"]
        )

    def test_invalid_license_last_five_not_digits(self):
        form = DriverCreationForm(
            data={
                "username": "u4",
                "password1": "Str0ng-Pa55!",
                "password2": "Str0ng-Pa55!",
                "first_name": "Neo",
                "last_name": "Driver",
                "license_number": "ABC12A4B",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Last 5 characters "
            "should be digits",
            form.errors["license_number"]
        )


class DriverLicenseUpdateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="edit_me",
            password="Str0ng-Pa55!",
            first_name="Ed",
            last_name="It_me",
            license_number="XYZ12345",
        )

    def test_valid_update(self):
        form = DriverLicenseUpdateForm(
            instance=self.user, data={"license_number": "QWE54321"}
        )
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.license_number, "QWE54321")

    def test_invalid_update_keeps_old_value(self):
        form = DriverLicenseUpdateForm(
            instance=self.user, data={"license_number": "bad"}
        )
        self.assertFalse(form.is_valid())
        self.user.refresh_from_db()
        self.assertEqual(self.user.license_number, "XYZ12345")


class LicenseValidatorUnitTest(TestCase):
    def test_validator_valid(self):
        self.assertEqual(
            validate_license_number("ABC12345"),
            "ABC12345"
        )

    def test_validator_length_error(self):
        with self.assertRaisesMessage(
                ValidationError,
                "License number should "
                "consist of 8 characters"
        ):
            validate_license_number("AB1234")

    def test_validator_uppercase_error(self):
        with self.assertRaisesMessage(
                ValidationError,
                "First 3 characters"
                " should be uppercase letters"
        ):
            validate_license_number("AbC12345")

    def test_validator_digits_error(self):
        with self.assertRaisesMessage(
                ValidationError,
                "Last 5 "
                "characters should be digits"
        ):
            validate_license_number("ABC12A4B")
