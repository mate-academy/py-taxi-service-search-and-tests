from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="FCQ",
            country="Poland",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="leo.messi",
            password="leomessipassword",
            first_name="Lionel",
            last_name="Messi",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="FCQ",
            country="Poland",
        )

        car = Car.objects.create(
            model="SP250",
            manufacturer=manufacturer,
        )
        self.assertEqual(
            str(car),
            car.model
        )

    def test_create_driver_with_license_number(self):
        username = "leo.messi"
        password = "test123"
        license_number = "ADM56984"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
