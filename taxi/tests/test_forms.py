from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverLicenseUpdateFormTest(TestCase):
    pass


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name_is_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "test123user",
            "password2": "test123user",
            "license_number": "SET876543",
            "first_name": "test first name",
            "last_name": "test last name"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
