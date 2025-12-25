from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test manufacturer ",
            country="USA"
        )

        expected = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="<PASSWORD>",
            first_name="Alex",
            last_name="White",
        )
        expected = (f"{driver.username} "
                    f"({driver.first_name} "
                    f"{driver.last_name})")
        self.assertEqual(str(driver), expected)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test manufacturer ",
            country="USA"
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        expected = f"{car.model}"
        self.assertEqual(str(car), expected)

    def test_create_driver_licence_number(self):
        username = "TestUser"
        password = "<PASSWORD>"
        license_number = "QWE12345"
        driver = get_user_model().objects.create(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertFalse(driver.check_password(password))
