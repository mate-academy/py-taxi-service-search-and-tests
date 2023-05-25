from taxi.forms import DriverCreationForm

from parameterized import parameterized
from django.test import TestCase


class FormsTest(TestCase):
    @parameterized.expand(
        [("test",
          "t1e2s3t4",
          "t1e2s3t4",
          "1-800-123-456",
          "Test",
          "Test",
          False),
         ("test", "t1e2s3t4", "t1e2s3t4", "12312347", "Test", "Test", False),
         ("test", "t1e2s3t4", "t1e2s3t4", "tst12347", "Test", "Test", False),
         ("test", "t1e2s3t4", "t1e2s3t4", "TSQWERTY", "Test", "Test", False),
         ("test", "t1e2s3t4", "t1e2s3t4", "T$T12347", "Test", "Test", False),
         ("test", "t1e2s3t4", "t1e2s3t4", "TST12347", "Test", "Test", True)],
        ids=[
            "not valid, phone number",
            "not valid, only digits, correct length",
            "not valid, lowercase letters",
            "not valid, only letters, correct length",
            "not valid, symbol used",
            "valid",
        ]
    )
    def test_driver_creation_form_with_license_number(
            self,
            username: str,
            password1: str,
            password2: str,
            license_number: str,
            first_name: str,
            last_name: str,
            result: bool
    ) -> None:
        form_data = {
            "username": username,
            "password1": password1,
            "password2": password2,
            "license_number": license_number,
            "first_name": first_name,
            "last_name": last_name,
        }
        form = DriverCreationForm(data=form_data)
        self.assertEqual(form.is_valid(), result)
