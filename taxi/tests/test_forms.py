from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_additional_fields(self):
        form_data = {
            "username": "test user",
            "license_number": "test number",
            "first_name": "test name",
            "last_name": "test last name",
            "password1": "test password",
            "password2": "test password",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
