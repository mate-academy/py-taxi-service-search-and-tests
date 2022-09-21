from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm

FORM_DATA = {
            "username": "username",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "First_name",
            "last_name": "Last_name",
            "license_number": "AAA12345"
        }


class TestForm(TestCase):
    def test_driver_creation_form_with_license_number_first_name_last_name(self):
        form = DriverCreationForm(data=FORM_DATA)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, FORM_DATA)

    def test_validation_license_number_should_consist_of_8_characters(self):
        FORM_DATA["license_number"] = "A1"
        form = DriverCreationForm(data=FORM_DATA)

        self.assertFalse(form.is_valid())

    def test_validation_license_number_first_3_characters_should_be_uppercase_letters(self):
        FORM_DATA["license_number"] = "aaa12345"
        form = DriverCreationForm(data=FORM_DATA)

        self.assertFalse(form.is_valid())

    def test_validation_license_number_last_5_characters_should_be_digits(self):
        FORM_DATA["license_number"] = "AAA*****"
        form = DriverCreationForm(data=FORM_DATA)

        self.assertFalse(form.is_valid())

    def test_private_create_driver(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="user12345"
        )
        self.client.force_login(self.user)

        self.client.post(reverse("taxi:driver-create"), data=FORM_DATA)
        driver = get_user_model().objects.get(id=2)

        self.assertEqual(driver.first_name, FORM_DATA["first_name"])
        self.assertEqual(driver.last_name, FORM_DATA["last_name"])
        self.assertEqual(driver.license_number, FORM_DATA["license_number"])
