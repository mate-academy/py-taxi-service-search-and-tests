from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    def test_license_number_is_valid(self):
        invalid_license_number = [
            "123", "abc", "zgmk123",
            "ABC12345", "BDF74654", "LKB89334"
        ]
        result = [False, False, False, True, True, True]

        for index, license_number in enumerate(invalid_license_number):
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
