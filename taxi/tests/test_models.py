from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer_ = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer_), f"{manufacturer_.name} {manufacturer_.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="username",
            password="user1234",
            first_name="test user",
            last_name="test user last name",
            license_number="TRD12232"
        )
        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        manufacturer_ = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        car = Car.objects.create(
            model="test model car",
            manufacturer=manufacturer_,
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_driver_license(self):
        username = "username"
        password = "user1234"
        license_number = "TRD12232"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
