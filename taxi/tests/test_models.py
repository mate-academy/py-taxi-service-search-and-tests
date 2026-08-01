from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Driver, Car, Manufacturer


class ModelTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="WV", country="German")
        car = Car.objects.create(model="test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="1234",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="WV", country="German")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "100000"
        license_number = "QWE12345"
        driver = get_user_model().objects.create_user(
            username=username, password=password, license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
