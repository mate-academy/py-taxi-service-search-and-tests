from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverCreationFormTest(TestCase):
    def test_driver_create_is_valid(self):
        form_data = {
            "username": "Test",
            "password1": "Test_1234",
            "password2": "Test_1234",
            "license_number": "TES12345",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
