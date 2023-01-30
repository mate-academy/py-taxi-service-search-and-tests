from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_adds_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user1234test",
            "password2": "user1234test",
            "first_name": "Firsttest",
            "last_name": "Lasttest",
            "license_number": "ASD12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def tests_license_number_validation_with_invalid_data(self):
        form_data = {
            "username": "new_user1",
            "password1": "user1234test",
            "password2": "user1234test",
            "first_name": "Firsttest",
            "last_name": "Lasttest",
            "license_number": "AsD12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
