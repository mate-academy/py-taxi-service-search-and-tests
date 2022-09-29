from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="ZAZ",
            country="Ukraine"
        )
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            email="test@vasa.ua",
            password="qwerty123",
            first_name="test_vasa",
            last_name="test_poroh"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="first", country="UK")
        car = Car.objects.create(
            model="ZAZ Vida",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), "ZAZ Vida")

    def test_driver_creation_with_lic_num(self):
        username = "test"
        password = "qwerty123"
        license_number = "ASD12345"
        driver = get_user_model().objects.create_user(
            username=username,
            email="test@vasa.ua",
            password=password,
            first_name="test_vasa",
            last_name="test_poroh",
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
