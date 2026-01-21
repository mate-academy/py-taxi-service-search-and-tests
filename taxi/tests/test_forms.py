from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTestCase(TestCase):
    def test_driver_creation_form_with_valid_data(self):
        form_data = {
            "username": "anton",
            "password1": "123Yyyyt",
            "password2": "123Yyyyt",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "IUI12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
