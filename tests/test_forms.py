from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_create(self):
        data = {
            "username": "test1",
            "password1": "test234567",
            "password2": "test234567",
            "license_number": "AAA12345",
            "first_name": "test3",
            "last_name": "test4",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)
