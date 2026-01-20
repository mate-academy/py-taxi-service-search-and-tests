from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def setUp(self):
        self.valid_form_data = {
            "username": "new.user",
            "password1": "usertest123",
            "password2": "usertest123",
            "first_name": "Test first_name",
            "last_name": "Test second_name",
            "license_number": "TST12345",
        }

    def test_driver_creation_form_with_license_number_is_valid(self):
        form = DriverCreationForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.valid_form_data)

    def test_invalid_license_number_formats(self):
        invalid_formats = ["ABC12", "12345678", "abc12345", "ABCccccc"]

        for invalid_license_number in invalid_formats:
            with self.subTest(invalid_license_number=invalid_license_number):
                form_data = self.valid_form_data.copy()
                form_data["license_number"] = invalid_license_number
                form = DriverCreationForm(data=form_data)
                self.assertFalse(form.is_valid())
                self.assertIn("license_number", form.errors)
