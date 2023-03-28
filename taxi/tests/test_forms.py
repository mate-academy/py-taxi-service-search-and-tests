from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverSearchForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_is_valid(self):
        form_data = {
            "username": "Marichka",
            "password1": "z54bvFG543",
            "password2": "z54bvFG543",
            "first_name": "Maria",
            "last_name": "Clinton",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
