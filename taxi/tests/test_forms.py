from django.test import TestCase

from taxi.forms import DriverCreationForm


class TestForms(TestCase):
    def test_driver_create_form_is_valid(self):
        """Test if  driver with first_name last_name license_number is valid"""
        form_data = {
            "username": "user",
            "password1": "user1234",
            "password2": "user1234",
            "first_name": "Test first_name",
            "last_name": "Test last_name",
            "license_number": "QWE12345",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
