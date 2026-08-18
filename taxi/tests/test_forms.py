from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name_is_valid(
        self,
    ):  # noqa: E501
        form_data = {
            "username": "new_user",
            "password1": "driver12345test",
            "password2": "driver12345test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ACD45678",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
