from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_new_params_is_valid(self):
        form_data = {
            "username": "user123",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "volodya",
            "last_name": "krivko",
            "license_number": "AAA12345",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
