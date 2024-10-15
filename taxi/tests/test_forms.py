from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "test_user"
        cls.password = "Test1234!"
        cls.first_name = "James"
        cls.last_name = "Bond"

    def create_form(self, license_number: str):
        form_data = {
            "username": self.username,
            "password1": self.password,
            "password2": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "license_number": license_number,
        }
        return DriverCreationForm(form_data)

    def test_valid_license_number(self):
        form = self.create_form("AAA12345")
        self.assertTrue(form.is_valid())

    def test_invalid_license_number_too_short(self):
        form = self.create_form("AA12345")
        self.assertFalse(form.is_valid())

    def test_invalid_license_number_format_uppercase(self):
        form = self.create_form("abc12345")
        self.assertFalse(form.is_valid())

    def test_invalid_license_number_format_digits(self):
        form = self.create_form("AAAABCDD")
        self.assertFalse(form.is_valid())
