from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_create_form(self):

        form_data = {
            "username": "name",
            "password1": "S3cur3P@ssw0rd!",
            "password2": "S3cur3P@ssw0rd!",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"],
                         "name"
                         )
        self.assertEqual(form.cleaned_data["first_name"],
                         "test first"
                         )
        self.assertEqual(form.cleaned_data["last_name"],
                         "test last"
                         )
        self.assertEqual(form.cleaned_data["license_number"],
                         "ABC12345"
                         )
