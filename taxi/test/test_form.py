from django.test import TestCase

from taxi.forms import DriverCreationForm


DATA = {
    "username": "test_name",
    "password1": "testpassword12345",
    "password2": "testpassword12345",
    "first_name": "First name",
    "last_name": "Last name",
    "license_number": "ABC12345"
}


class FormTest(TestCase):
    def test_driver_creation_form_if_add_custom_fields(self):

        form = DriverCreationForm(
            data=DATA
        )
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, DATA)

    def test_custom_license_number_validator(self):
        data = DATA.copy()
        for license_number in ["Abc12345", "ABC12L45", "ABC1234"]:
            data["license_number"] = license_number
            form = DriverCreationForm(
                data=data
            )
            self.assertFalse(form.is_valid())
