from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "test_user",
            "password1": "user1234",
            "password2": "user1234",
            "license_number": "QWE12345",
            "first_name": "Jason",
            "last_name": "Statham"
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update_form(self):
        form_data = {"license_number": "ASD12345"}

        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
