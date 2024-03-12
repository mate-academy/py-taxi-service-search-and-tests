from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer


class ManufacturerTest(TestCase):
    def test_manufacturer_str_method(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="VAZ",
            country="Ukraine"
        )

        self.assertEqual(str(manufacturer), "VAZ Ukraine")


class DriverTest(TestCase):
    def test_driver_str_method(self) -> None:
        driver = get_user_model().objects.create_user(
            username="krixnjee",
            password="12333",
            first_name="Serhii",
            last_name="Haiduchyk",
            license_number="ASD12345"
        )

        self.assertEqual(
            str(driver),
            "krixnjee (Serhii Haiduchyk)"
        )
