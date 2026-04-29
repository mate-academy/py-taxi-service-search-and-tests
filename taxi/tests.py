from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Driver, Car, Manufacturer


class ModelsTeste(TestCase):
    def test_driver_str(self):
        driver = Driver.objects.create(
            username="test",
            first_name="John",
            last_name="Doe"
        )
        self.assertEqual(str(driver),
                         f"{driver.username} "
                         f"({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="John"
        )
        car = Car.objects.create(model="test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="John"
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_create_driver(self):
        username = "test"
        password = "test123"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
