from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_with_license_number_first_name_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "IKJ23456",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])



