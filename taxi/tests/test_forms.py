from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "my987test",
            "password2": "my987test",
            "first_name": "First_test",
            "last_name": "Last_test",
            "license_number": "TES12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
