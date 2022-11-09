from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_and_names(self):
        form_data = {
            "username": "JohnDoe",
            "password1": "123qwe12",
            "password2": "123qwe12",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "ABC97856",
            "avatar": "default.png",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
