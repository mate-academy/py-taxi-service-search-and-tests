from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def setUp(self):
        self.valid_form_data = {
            "username": "test_name",
            "license_number": "NNN12345",
            "first_name": "test_first",
            "last_name": "test_last",
            "password1": "test_password",
            "password2": "test_password",
        }

    def create_form_with_data(self, form_data):
        form = DriverCreationForm(data=form_data)
        return form

    def test_create_driver_form_with_valid_data(self):
        form = self.create_form_with_data(self.valid_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.valid_form_data)

    def test_create_driver_form_invalid_len_numbers_license_number(self):
        invalid_data = self.valid_form_data.copy()
        invalid_data["license_number"] = "NNN1234"
        form = self.create_form_with_data(invalid_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, invalid_data)

    def test_create_driver_form_invalid_letter_license_number(self):
        invalid_data = self.valid_form_data.copy()
        invalid_data["license_number"] = "aQN12342"
        form = self.create_form_with_data(invalid_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, invalid_data)

    def test_create_driver_form_invalid_len_letters_license_number(self):
        invalid_data = self.valid_form_data.copy()
        invalid_data["license_number"] = "QW12342"
        form = self.create_form_with_data(invalid_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, invalid_data)
