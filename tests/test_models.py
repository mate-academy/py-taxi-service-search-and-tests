from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer


class ManufacturerTest(TestCase):
    def test_manufacturer_str_method(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.assertEqual(str(manufacturer), "BMW Germany")


class DriverTest(TestCase):
    def test_driver_str_method(self) -> None:
        driver = get_user_model().objects.create_user(
            username="interjkee",
            password="12345",
            first_name="Alex",
            last_name="Chalaidiuk",
            license_number="ABC12345"
        )

        self.assertEqual(
            str(driver),
            "interjkee (Alex Chalaidiuk)"
        )
