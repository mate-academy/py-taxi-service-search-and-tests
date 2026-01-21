from django.test import TestCase
from taxi.forms import DriverCreationForm


class TestForm(TestCase):
    def test_driver_creation_form_with_license_number_is_valid(self):
        form_data = {
            "username": "Test",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "first_name": "FirstTest",
            "last_name": "SecondTest",
            "license_number": "TTT23456",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"],
                         form_data["username"])
        self.assertEqual(form.cleaned_data["license_number"],
                         form_data["license_number"])
        self.assertEqual(form.cleaned_data["first_name"],
                         form_data["first_name"])
        self.assertEqual(form.cleaned_data["last_name"],
                         form_data["last_name"])
