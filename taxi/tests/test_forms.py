from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    form_data = {
        "username": "test_username",
        "password1": "1234qwerasdf",
        "password2": "1234qwerasdf",
        "license_number": "TST45678",
        "first_name": "first",
        "last_name": "last",
    }

    def test_form_is_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_license_number_less_characters(self):
        self.form_data["license_number"] = "TST4567"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_license_number_more_characters(self):
        self.form_data["license_number"] = "TST456789"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_license_number_first_characters_wrong(self):
        self.form_data["license_number"] = "tst456789"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_license_number_last_characters_not_digits(self):
        self.form_data["license_number"] = "TST4567aa"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
