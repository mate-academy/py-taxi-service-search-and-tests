from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_added_fields(self):
        form_data = {
            "username": "testUsername",
            "license_number": "ISA12345",
            "first_name": "test first name",
            "last_name": "test last name",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
