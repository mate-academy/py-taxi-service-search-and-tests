from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormTests(TestCase):
    @pytest.mark.parametrize("license_number, expected_result", [
        ("111", False),
        ("aaa", False),
        ("aaa11111", False),
        ("aaaaaaaa", False),
        ("AAA11111", True),
    ])
    def test_license_number_is_valid(self):
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
