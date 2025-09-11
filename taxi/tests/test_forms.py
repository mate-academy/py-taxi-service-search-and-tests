from django.template.defaultfilters import first
from django.test import TestCase

from taxi.models import Driver


class DriverFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Driver.objects.create(
            license_number="RFC34532"
        )

    def setUp(self):
        self.driver = Driver.objects.get(pk=1)

    def test_validate_license_number_len_equal_8(self):
        license_d = self.driver.license_number
        self.assertEqual(len(license_d), 8)

    def test_license_number_first_3_letters_are_upper_and_alpha(self):
        first_3 = self.driver.license_number[:3]
        self.assertTrue(first_3.isupper() and first_3.isalpha())

    def test_license_number_last_5_letters_are_digits(self):
        last_5 = self.driver.license_number[3:]
        self.assertTrue(last_5.isdigit())
