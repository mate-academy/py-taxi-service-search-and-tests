from django.contrib.auth import get_user_model
from django.test import (TestCase)

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacture_str(self):
        manufacture = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        self.assertEqual(
            str(manufacture),
            f"{manufacture.name} {manufacture.country}"
        )

    def test_driver_info(self):
        username = "test_username"
        first_name = "test_first_name"
        last_name = "test_last_name"
        license_number = "AAA1111"
        driver = Driver.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
        )
        self.assertEqual(str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
                         )

    def test_car_info(self):
        driver = Driver.objects.create(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="AAA43434"
        )
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        model = "test_model"
        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer
                                 )
        car.drivers.add(driver)
        car.save()
        self.assertEqual(str(car), f"{car.model}")
