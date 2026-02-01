from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def test_manufacturer_str(self):
        manuf = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Germany",
        )
        self.assertEqual(
            str(manuf),
            f"{manuf.name} {manuf.country}"
        )


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manuf = Manufacturer.objects.create(name="Test Manufacturer")
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manuf
        )
        driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="test_driver1",
            license_number="AAA11111"
        )
        driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="test_driver2",
            license_number="AAA22222"
        )
        car.drivers.add(driver1)
        car.drivers.add(driver2)

    def test_car_str(self):
        car = Car.objects.get(id=1)
        self.assertEqual(str(car), "Test Model")

    def test_car_drivers_quantity(self):
        car = Car.objects.get(id=1)
        drivers = car.drivers.all()
        self.assertEqual(len(drivers), 2)


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="driver1",
            first_name="Boris",
            last_name="Britva",
            password="test_driver1",
            license_number="AAA11111"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_license_number_length_equal_8(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(len(driver.license_number), 8)

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(
            driver.get_absolute_url(),
            "/drivers/1/"
        )
