from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )
        self.assertEquals(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test_username",
            password="test1234",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.assertEquals(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        self.assertEquals(
            str(car),
            car.model
        )

    def test_create_driver_with_license_number(self):
        username = "test_username"
        password = "test1234"
        license_number = "test_license_number"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )

        self.assertEquals(driver.username, username)
        self.assertEquals(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
