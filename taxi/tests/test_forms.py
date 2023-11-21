from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_license_number_is_valid(self):
        license_numbers = [
            "111", "aaa", "aaa11111", "aaaaaaaa", "AAA11111",
        ]
        result = [False, False, False, False, True]

        for index, license_number in enumerate(license_numbers):
            form = DriverCreationForm(
                data={
                    "username": "driver",
                    "password1": "NotCommonPassword123",
                    "password2": "NotCommonPassword123",
                    "first_name": "TestName",
                    "last_name": "Last_name",
                    "license_number": license_number
                }
            )
            print(form.is_valid())
            self.assertEqual(form.is_valid(), result[index])
