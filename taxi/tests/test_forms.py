from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_firs_last_name_is_valid(self):
        form_data = {
            "username": "driver",
            "password1": "pwd12345pwd",
            "password2": "pwd12345pwd",
            "first_name": "Tester",
            "last_name": "Testenko",
            "license_number": "TST56789"
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
