from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "driver_1",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "John",
            "last_name": "Smith",
            "license_number": "ADM56984"
        }

    def test_driver_creation_form_with_fields_is_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)
