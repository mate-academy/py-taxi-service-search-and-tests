from django.core.exceptions import ValidationError
from django.test import TestCase
from taxi.models import Driver
from taxi.forms import validate_license_number


class TestLisenseNumberValidation(TestCase):
    def test_driver_license_number_validation(self):
        driver = Driver.objects.create(
            username="testusername",
            first_name="testfirst",
            last_name="testlast",
            license_number="ABC12345",
        )
        driver2 = Driver.objects.create(
            username="testusername2",
            first_name="testfirst2",
            last_name="testlast2",
            license_number="ASJNHX712",
        )
        driver3 = Driver.objects.create(
            username="testusername3",
            first_name="testfirst3",
            last_name="testlast3",
            license_number="ABCD1234",
        )

        self.assertTrue(validate_license_number(driver.license_number))
        with self.assertRaises(ValidationError):
            validate_license_number(driver2.license_number)
        with self.assertRaises(ValidationError):
            validate_license_number(driver3.license_number)
