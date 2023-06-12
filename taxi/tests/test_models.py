from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        test_manufacturer = Manufacturer.objects.create(name="test")

        self.assertEqual(
            str(test_manufacturer),
            f"{test_manufacturer.name} {test_manufacturer.country}"
        )

    def test_driver_str(self):
        test_driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last",
            license_number="TST12345"
        )

        self.assertEqual(
            str(test_driver),
            f"{test_driver.username} "
            f"({test_driver.first_name} "
            f"{test_driver.last_name})"
        )

    def test_car_drivers_assigned(self):
        test_manufacturer = Manufacturer.objects.create(name="test")
        test_driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last",
            license_number="TST12345"
        )

        test_driver_second = get_user_model().objects.create_user(
            username="test2",
            password="test12345",
            first_name="Test first",
            last_name="Test last",
            license_number="TST67890"
        )

        test_car = Car.objects.create(
            model="Test",
            manufacturer=test_manufacturer,
        )

        test_driver.cars.add(test_car)
        test_driver_second.cars.add(test_car)

        self.assertEqual(
            test_driver,
            test_car.drivers.get(username=test_driver.username)
        )
        self.assertEqual(
            test_driver_second,
            test_car.drivers.get(username=test_driver_second.username)
        )
