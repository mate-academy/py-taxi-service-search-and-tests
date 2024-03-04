from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def setUp(self):
        self.test_password = "testPass1"
        self.form_data = {
            "username": "driver",
            "password1": self.test_password,
            "password2": self.test_password,
            "first_name": "John",
            "last_name": "Smith",
            "license_number": "DRI12345"
        }

    def test_driver_creation_form_custom_fields(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_creation_validation(self):
        self.form_data["license_number"] = "not12345"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_update_validation(self):
        self.form_data["license_number"] = "notValid"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
