from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import validate_license_number


class FormTest(TestCase):

    def test_validation_license_number_ok(self):
        form = validate_license_number("ABC12345")
        self.assertEqual(form, "ABC12345")

    def test_license_number_too_short(self):
        with self.assertRaises(ValidationError) as cm:
            validate_license_number("AB12")
        self.assertIn("should consist of 8 characters", str(cm.exception))

    def test_license_number_digits_control(self):
        with self.assertRaises(ValidationError) as cm:
            validate_license_number("ABBFGTQW")
        self.assertIn("should be digits", str(cm.exception))
