from django.db import IntegrityError
from django.test import TestCase

from taxi.models import Driver


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="Test",
            password="1234",
            license_number="ABC12345"
        )

    def test_license_number_label(self):
        field_label = self.driver._meta.get_field(
            "license_number"
        ).verbose_name
        self.assertEqual(field_label, "license number")

    def test_license_number_max_length(self):
        max_length = self.driver._meta.get_field("license_number").max_length
        self.assertEqual(max_length, 255)

    def test_class_verbose_name(self):
        verbose_name = self.driver._meta.verbose_name
        self.assertEqual(verbose_name, "driver")

    def test_class_verbose_name_plural(self):
        verbose_name_plural = self.driver._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, "drivers")

    def test_license_number_unique(self):
        try:
            Driver.objects.create_user(
                username="Test1",
                password="12345",
                license_number="ABC12345"
            )
            assert False
        except IntegrityError:
            assert True

    def test_driver_str(self):
        expected = (f"{self.driver.username} "
                    f"({self.driver.first_name} "
                    f"{self.driver.last_name})")
        self.assertEqual(expected, str(self.driver))

    def test_get_absolute_url(self):
        expected = "/drivers/1/"
        self.assertEqual(expected, self.driver.get_absolute_url())
