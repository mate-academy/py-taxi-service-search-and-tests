from django.test import TestCase

from taxi.forms import DriverCreationForm


class TestDriverCreationForm(TestCase):
    def test_driver_form_intro(self):
        form_data = {
            "username": "driver",
            "license_number": "MOR12345",
            "first_name": "first",
            "last_name": "last",
            "password1": "admin-1234",
            "password2": "admin-1234",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form_data, form.cleaned_data)
