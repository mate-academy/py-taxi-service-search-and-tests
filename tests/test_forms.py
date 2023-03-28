from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_driver_creation_with_correct_license_number(self):
        data = {
            "username": "test2",
            "password1": "test-!@1234",
            "password2": "test-!@1234",
            "first_name": "first name",
            "last_name": "last name",
            "license_number": "ADM56984"
        }

        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data, data)

    def test_driver_creation_with_wrong_license_number(self):
        data = {
            "username": "test2",
            "password1": "test-!@1234",
            "password2": "test-!@1234",
            "first_name": "first name",
            "last_name": "last name",
            "license_number": "ADM56984"
        }

        pass  # mask linter warning

        data["license_number"] = "ADM56984-"
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

        data["license_number"] = "ADM569845"
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

        data["license_number"] = "aDM56984"
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

        data["license_number"] = "12356984"
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)
