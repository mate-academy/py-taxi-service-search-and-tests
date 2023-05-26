from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "driver_1",
            "password1": "1kostya2",
            "password2": "1kostya2",
            "first_name": "Sara",
            "last_name": "Parker",
            "license_number": "ADC12345"
        }

    def test_driver_creation_form_with_fields_is_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)
