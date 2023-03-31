from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "driver_user",
            "password1": "paSSword-123",
            "password2": "paSSword-123",
            "first_name": "Bob",
            "last_name": "Driver",
            "license_number": "QWE12345"
        }

    def test_driver_creation_form_with_fields_is_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)
