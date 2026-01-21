from django.test import TestCase
from taxi.models import Manufacturer
from taxi.forms import validate_license_number
from django.core.exceptions import ValidationError


class ManufacturerModelTests(TestCase):
    def test_str(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        self.assertEqual(str(manufacturer), "Ford USA")


class DriverLicenseValidatorTests(TestCase):
    def test_validate_license_number_success(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_validate_license_number_length_error(self):
        with self.assertRaises(ValidationError):
            validate_license_number("AB12345")

    def test_validate_license_number_prefix_format_error(self):
        with self.assertRaises(ValidationError):
            validate_license_number("AbC12345")
        with self.assertRaises(ValidationError):
            validate_license_number("A1C12345")

    def test_validate_license_number_suffix_digits_error(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC12A45")
