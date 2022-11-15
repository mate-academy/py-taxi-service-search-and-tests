from django.test import TestCase

from taxi.forms import CookCreationForm


class FormsTest(TestCase):
    def test_driver_creation_with_correct_data(self):
        form_data = {
            "username": "test_name",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "firstname",
            "last_name": "lastname",
            "license_number": "AAA12345",
        }
        form = CookCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_with_incorrect_data(self):
        incorrect_license = ["AA123456", "AABB", "AAA1234"]
        for license_number in incorrect_license:
            with self.subTest(license_number=license_number):
                form_data = {
                    "username": "test_name",
                    "password1": "test12345",
                    "password2": "test12345",
                    "first_name": "firstname",
                    "last_name": "lastname",
                    "license_number": license_number,
                }
                form = CookCreationForm(form_data)

                self.assertFalse(form.is_valid())
                self.assertNotEqual(form.cleaned_data, form_data)
