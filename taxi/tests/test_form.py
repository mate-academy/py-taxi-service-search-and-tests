from django.test import TestCase

from taxi.forms import DriverCreationForm


class TestForm(TestCase):
    def test_driver_with_license_number_is_valid(self):
        data = {
            "username": "test",
            "password1": "test1234",
            "password2": "test1234",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "license_number": "Test License"
        }

        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, data)
