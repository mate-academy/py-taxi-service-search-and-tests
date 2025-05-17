from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user1",
            "password1": "user_password1",
            "password2": "user_password1",
            "first_name": "first_name1",
            "last_name": "last_name1",
            "license_number": "VDD12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(
            form.cleaned_data["username"] == form_data["username"]
        )
        self.assertTrue(
            form.cleaned_data["first_name"] == form_data["first_name"]
        )
        self.assertTrue(
            form.cleaned_data["last_name"] == form_data["last_name"]
        )
        self.assertTrue(
            form.cleaned_data["license_number"] == form_data["license_number"]
        )
        form_data["license_number"] = "12345"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
