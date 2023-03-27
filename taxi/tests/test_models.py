from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        name_ = Manufacturer.objects.create(
            name="test",
            country="Test"
        )
        self.assertEqual(str(name_), f"{name_.name} {name_.country}")

    def test_driver_str(self):

        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last"
        )

        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name}"
                                      f"{driver.last_name})")

    def test_car_str(self):
        name_ = Manufacturer.objects.create(
            name="test",
            country="Test"
        )
        car = Car.objects.create(
            model="Testing",
            manufacturer=name_
        )

        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test12345"
        license_number = "test licence_number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
