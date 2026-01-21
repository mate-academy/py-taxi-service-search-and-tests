from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="VAG",
            country="Germany"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="username",
            first_name="first_name",
            last_name="last_name"

        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        license_number = "QWE12312"
        username = "username1"
        password = "password1"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.check_password(password), True)

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="username1",
            password="password1",
        )
        self.assertEqual(
            driver.get_absolute_url(),
            "/drivers/1/"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="VAG",
            country="Germany"
        )
        car = Car.objects.create(
            model="model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)
