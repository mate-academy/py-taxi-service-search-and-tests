from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):

    def test_driver_creation_form_with_license_is_valid(self):
        form_data = {
            "username": "supersecret",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "John",
            "last_name": "Smith",
            "license_number": "ABC12345",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
