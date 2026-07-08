from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test_Name",
            country="Test_Country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver(self):
        driver = get_user_model().objects.create(
            username="test_user",
            password="test_password",
            first_name="first_name",
            last_name="last_name"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Test_Name",
            country="Test_Country"
        )
        driver = get_user_model().objects.create(
            username="test_user",
            password="test_password",
            first_name="first_name",
            last_name="last_name"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        car.drivers.set([driver])
        self.assertEqual(
            str(car),
            car.model
        )

    def test_create_driver_license(self):
        username = "test_user"
        password = "test_password"
        license_num = "ASD11111"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_num
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_num)
        self.assertTrue(driver.check_password(password))
