from django.test import TestCase

from ..forms import DriverCreationForm


class FormsTests(TestCase):
    def test_form_valid(self):
        form_data = {
            "username": "johny",
            "license_number": "QWE12345",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "Strongpassword123!",
            "password2": "Strongpassword123!",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
