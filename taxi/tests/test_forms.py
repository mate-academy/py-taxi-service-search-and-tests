from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def setUp(self):
        self.valid_form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "DAS12352"
        }

    def test_driver_creation_form_with_valid_data(self):
        form_data = self.valid_form_data
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_with_invalid_license_number(self):
        form_data = self.valid_form_data.copy()
        form_data["license_number"] = "DA12352"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
