from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_first_name_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user1234",
            "password2": "user1234",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "DUS25131"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
