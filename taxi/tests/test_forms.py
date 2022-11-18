from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_drive_creation_form_with_license_number_is_valid(self):
        form_data = {
            "username": "username",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "test_name",
            "last_name": "test_surname",
            "license_number": "AAA00001",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
