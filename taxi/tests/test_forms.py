from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name_is_valid(
            self):
        form_data = {
            "username": "newuser",
            "password1": "user12test",
            "password2": "user12test",
            "license_number": "TES12345",
            "first_name": "Testfirst",
            "last_name": "Testlast",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

        self.assertEqual(form.cleaned_data["username"], form_data["username"])
        self.assertEqual(form.cleaned_data["first_name"],
                         form_data["first_name"])
        self.assertEqual(form.cleaned_data["last_name"],
                         form_data["last_name"])
        self.assertEqual(
            form.cleaned_data["license_number"], form_data["license_number"]
        )
