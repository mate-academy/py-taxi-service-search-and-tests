from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_license_number_first_last_name_is_valid(
            self):
        form_data = {
            "username": "admin",
            "password1": "admin12345",
            "password2": "admin12345",
            "license_number": "TES12345",
            "first_name": "Test first",
            "last_name": "Test last"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="newtest",
            password="newtest1234",
            license_number="NEW12345"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "newuser",
            "password1": "user12345",
            "password2": "user12345",
            "license_number": "USE12345",
            "first_name": "Test first",
            "last_name": "Test last"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.license_number, form_data["license_number"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])

    def test_license_number_errors(self):
        license_numbers = [
            "XYZ123456",
            "AB123456",
            "abc12345",
            "ABCD1234"
        ]
        for license_number in license_numbers:

            form = DriverCreationForm(
                data={
                    "username": "testuser",
                    "password1": "testuser1234",
                    "password2": "testuser1234",
                    "license_number": license_number,
                    "first_name": "John",
                    "last_name": "Doe",
                }
            )
            self.assertFalse(form.is_valid())
            self.assertIn("license_number", form.errors)
