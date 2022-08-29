from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.forms import DriverCreationForm
from django.urls import reverse


class FormTests(TestCase):
    def test_driver_creation_form_with_license_number(self):
        form_data = {
            "username": "test_username",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "first_name_test",
            "last_name": "last_name_test",
            "license_number": "QWF12345",

        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test_username", "user123test"
        )
        self.client.force_login(self.user)

    def test_create_drivers(self):
        format_data = {
            "username": "test_username",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "first_name_test",
            "last_name": "last_name_test",
            "license_number": "QWF12345",

        }
        self.client.post(reverse("taxi:driver-create"), date=format_data)
        new_user = get_user_model().objects.get(username=format_data["username"])
        self.assertEqual(new_user.username, format_data["username"])
