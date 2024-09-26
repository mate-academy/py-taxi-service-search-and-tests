from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(country="test")
        self.assertRegex(str(manufacturer), manufacturer.country)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create(
            username="test",
            first_name="test_first",
            last_name="test_last"
        )
        self.assertEqual(
            driver.get_absolute_url(), "/drivers/1/"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test")
        driver = get_user_model().objects.create(
            username="test",
            first_name="test_first",
            last_name="test_last",
        )
        car = Car.objects.create(model="test", manufacturer=manufacturer)
        car.drivers.set([driver])

        self.assertEqual(str(car), "test")
