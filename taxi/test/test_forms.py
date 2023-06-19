from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverCreationFormTest(TestCase):
    def test_driver_creat_form(self):
        form_data = {
            "username": "new_user",
            "password1": "user12345",
            "password2": "user12345",
            "first_name": "User first",
            "last_name": "User last",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form_data, form.cleaned_data)
