from django.test import TestCase, override_settings

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):

    @override_settings(AUTH_PASSWORD_VALIDATORS=[])
    def test_driver_creation_form_with_license_number_name_is_valid(self):
        form_data = {
            "username": "test",
            "license_number": "AAA23345",
            "first_name": "test_first",
            "last_name": "test_last",
            "password1": "Test123",
            "password2": "Test123",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
