from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form(self) -> None:
        form_data = {
            "username": "test",
            "password1": "pass1234Q",
            "password2": "pass1234Q",
            "first_name": "first name",
            "last_name": "last name",
            "license_number": "AAA11111"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
