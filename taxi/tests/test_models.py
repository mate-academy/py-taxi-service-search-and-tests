from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class CarModelTest(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)


class DriverModelTest(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="Test",
            password="<test1234",
            first_name="Test First",
            last_name="Test Last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="Test",
            password="test1234"
        )
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")
