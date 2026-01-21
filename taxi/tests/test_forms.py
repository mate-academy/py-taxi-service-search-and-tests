from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_additional_fields_is_valid(self):
        form_data = {
            "username": "test_username",
            "password1": "testpassword12345",
            "password2": "testpassword12345",
            "first_name": "test first name",
            "last_name": "test last name",
            "license_number": "ADR12345",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
