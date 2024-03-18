from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class TestModels(TestCase):
    USERNAME = "test_user"
    FIRST_NAME = "test_firstname"
    LAST_NAME = "test_last_name"
    PASSWORD = "test_password123"
    LICENSE_NUMBER = "TES12345"
    MANUFACTURER_NAME = "test name"
    MANUFACTURER_COUNTRY = "test country"
    CAR_MODEL = "TEST MODEL"

    def setUp(self):
        driver = Driver.objects.create_user(
            username=self.USERNAME,
            password=self.PASSWORD,
            last_name=self.LAST_NAME,
            first_name=self.FIRST_NAME,
            license_number=self.LICENSE_NUMBER
        )
        manufacturer = Manufacturer.objects.create(
            name=self.MANUFACTURER_NAME,
            country=self.MANUFACTURER_COUNTRY
        )
        car = Car.objects.create(
            manufacturer=manufacturer,
            model=self.CAR_MODEL
        )
        car.drivers.add(driver)

    def test_manufacturer_model(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(manufacturer.name, self.MANUFACTURER_NAME)
        self.assertEqual(manufacturer.country, self.MANUFACTURER_COUNTRY)

    def test_str_manufacturer(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_model(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(driver.first_name, self.FIRST_NAME)
        self.assertEqual(driver.last_name, self.LAST_NAME)
        self.assertTrue(driver.check_password(self.PASSWORD))
        self.assertEqual(driver.username, self.USERNAME)
        self.assertEqual(driver.license_number, self.LICENSE_NUMBER)

    def test_str_driver(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(
            str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_str_car(self):
        car = Car.objects.get(id=1)
        self.assertEqual(str(car), car.model)

    def test_car_model(self):
        car = Car.objects.get(id=1)
        driver = get_user_model().objects.get(id=1)
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(car.manufacturer, manufacturer)
        self.assertTrue(driver in car.drivers.all())
