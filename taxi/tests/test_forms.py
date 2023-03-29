from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_number_is_valid(self):

        form_data = {
            "username": "test",
            "password1": "t1e2s3t4",
            "password2": "t1e2s3t4",
            "license_number": "TST12347",
            "first_name": "Test",
            "last_name": "Test",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form.data)
