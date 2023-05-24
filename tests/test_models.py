from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ManufacturerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="VAG",
            country="Germany"
        )

    def test_model_manufacturer_str_(self):
        manufacturer = Manufacturer.objects.get(id=1)
        expected_str = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected_str)


class DriverTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123321123",
            first_name="John",
            last_name="Doe",
            license_number="ADS12333"
        )

        cls.driver = driver

    def test_model_str_(self):
        expected_str = "test (John Doe)"
        self.assertEqual(str(self.driver), expected_str)

    def test_get_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), "/drivers/1/")

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test123321123"
        license_number = "ADS12333"

        self.assertEqual(self.driver.username, username)
        self.assertTrue(self.driver.check_password(password))
        self.assertEqual(self.driver.license_number, license_number)


class CarTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="VAG",
            country="Germany"
        )
        Car.objects.create(
            model="Audi",
            manufacturer_id=1,
        )

    def test_model_car_str(self):
        car = Car.objects.get(id=1)
        self.assertEqual(str(car), "Audi")

    def test_model_car_has_manufacturer(self):
        car = Car.objects.get(id=1)
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(car.manufacturer, manufacturer)
