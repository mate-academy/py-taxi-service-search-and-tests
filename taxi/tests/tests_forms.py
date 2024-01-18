from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsDriverTest(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "test_user",
            "password1": "Pass12345",
            "password2": "Pass12345",
            "license_number": "QWE12345",
            "first_name": "test first",
            "last_name": "test last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)
