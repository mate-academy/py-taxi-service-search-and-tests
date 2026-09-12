from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "BCA12345",
        }

    def test_if_driver_creation_have_valid_data(self):
        form_data = self.form_data.copy()
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_license_short(self):
        form_data = self.form_data.copy()
        form_data["license_number"] = "BCA123"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_small_first_letters(self):
        form_data = self.form_data.copy()
        form_data["license_number"] = "abc12345"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_fourth_is_letter(self):
        form_data = self.form_data.copy()
        form_data["license_number"] = "BCAX2345"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
