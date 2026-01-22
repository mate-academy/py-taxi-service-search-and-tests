from django.test import TestCase
from taxi.forms import DriverCreationForm


class DriverCreationFormTest(TestCase):

    def test_driver_create_with_license_number_first_name_last_name(self):

        form_data = {
            "username": "test",
            "password1": "test_1234",
            "password2": "test_1234",
            "license_number": "TES12345",
            "first_name": "testfirstname",
            "last_name": "testlastname",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
