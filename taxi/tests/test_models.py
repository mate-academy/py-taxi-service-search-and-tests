from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="USA")
        self.assertEquals(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="USA")
        car = Car.objects.create(model="test", manufacturer=manufacturer)
        self.assertEquals(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test1234",
            first_name="testsit",
            last_name="12test",
        )
        self.assertEquals(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license(self):
        username = "test"
        password = "Test1234"
        license_number = "tumut123"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
