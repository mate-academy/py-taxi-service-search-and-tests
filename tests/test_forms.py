from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, validate_license_number


class FormsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)

    def test_create_author(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "First name test",
            "last_name": "Last name test",
            "license_number": "TST12345",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_validate_license_should_consist_of_8_characters(self):
        self.assertRaisesMessage(
            ValidationError,
            "License number should consist of 8 characters",
            validate_license_number,
            "TST1234",
        )

    def test_validate_license_number_first_3_characters_should_be_uppercase(
        self,
    ):
        self.assertRaisesMessage(
            ValidationError,
            "First 3 characters should be uppercase letters",
            validate_license_number,
            "tST12345",
        )

    def test_validate_license_number_last_5_characters_should_be_digits(self):
        self.assertRaisesMessage(
            ValidationError,
            "Last 5 characters should be digits",
            validate_license_number,
            "TST1234S",
        )
