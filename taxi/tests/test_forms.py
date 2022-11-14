from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_license_number_name_is_valid(self):
        form_data = {
            "username": "testuser",
            "password1": "Testpassword123",
            "password2": "Testpassword123",
            "first_name": "first test",
            "last_name": "last test",
            "license_number": "QEK12114",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
