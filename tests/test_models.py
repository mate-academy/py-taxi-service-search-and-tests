from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )

        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first",
            last_name="test_last",
            password="admin12345",
        )

        self.assertEqual(str(driver),
                         f"{driver.username} ({driver.first_name} "
                         f"{driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )

        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), car.model)

    def test_create_driver_license_number(self):
        username = "test_username"
        first_name = "test_first"
        last_name = "test_last"
        password = "admin12345"
        license_number = "test_license"
        driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            license_number=license_number,
        )

        self.assertEqual(str(driver.username), username)
        self.assertEqual(str(driver.first_name), first_name)
        self.assertEqual(str(driver.last_name), last_name)
        self.assertEqual(str(driver.license_number), license_number)
        self.assertTrue(driver.check_password(password))
