from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_driver_form_with_extra_data_is_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "pwdUser12345",
            "password2": "pwdUser12345",
            "first_name": "first_name_test",
            "last_name": "last_name_test",
            "license_number": "ABC12345",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
