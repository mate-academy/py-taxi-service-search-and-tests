from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "test_user_name",
            "password1": "test_pass123",
            "password2": "test_pass123",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "license_number": "QWE15975"
        }

    def test_driver_creation_form_with_fields_is_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)
