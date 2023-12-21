from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer, Driver


class ModelsTests(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="tY4HPQZ7xxjs",
            first_name="test_first",
            last_name="test_last",
            license_number="ABC12345",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create(
            username="test",
            password="tY4HPQZ7xxjs",
            first_name="test_first",
            last_name="test_last",
            license_number="ABC12345",
        )

        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test")
        driver = get_user_model().objects.create(
            username="test",
            password="tY4HPQZ7xxjs",
            first_name="test_first",
            last_name="test_last",
            license_number="ABC12345",
        )
        car = Car.objects.create(model="test", manufacturer=manufacturer)
        car.drivers.set([driver])

        self.assertEqual(str(car), "test")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="Ukraine"
        )

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )
