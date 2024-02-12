from django.test import TestCase

from taxi.forms import DriverCreationForm


class DriverFormsTest(TestCase):
    def setUp(self):
        super().setUp()
        self.form_data = {
            "username": "test_user",
            "password1": "ValidPassword123!",
            "password2": "ValidPassword123!",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": ""
        }

    def test_creation_valid(self):
        self.form_data["license_number"] = "TST12345"
        form = DriverCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, self.form_data)

    def test_wrong_lower_case(self):
        self.form_data["license_number"] = "tST12345"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())

    def test_wrong_number_in_first_three_characters(self):
        self.form_data["license_number"] = "T1T12345"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())

    def test_wrong_more_than_eight_characters(self):
        self.form_data["license_number"] = "TST1234567"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())

    def test_wrong_less_than_eight_characters(self):
        self.form_data["license_number"] = "TST123"
        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
