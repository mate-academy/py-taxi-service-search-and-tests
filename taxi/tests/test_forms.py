from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_create(self):
        form_data = {
            "username": "testuser",
            "password1": "MyStr0ngP@ss",
            "password2": "MyStr0ngP@ss",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "ABC11111",
        }
        form = DriverCreationForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
