from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="name",
            country="country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test_username",
            password="test_p",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car = Car.objects.create(
            model="test_m",
            manufacturer=manufacturer,
        )
        self.assertEqual(
            str(car),
            car.model
        )

    def test_driver_with_license_number(self):
        username = "test_u"
        password = "test_p"
        license_number = "UUU11111"
        driver = get_user_model().objects.create(
            username=username,
            password=password,
            license_number=license_number,
        )

        self.assertEqual(driver.username, username)
        self.assertEqual(driver.password, password)
        self.assertEqual(driver.license_number, license_number)
