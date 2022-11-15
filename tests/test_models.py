from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BSJW5",
            country="Juwos"
        )

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Hiso",
            first_name="Jimmy",
            last_name="Likoswu",
            license_number="KWQ12345"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BSJW5",
            country="Juwos"
        )

        car = Car.objects.create(
            model="Opel",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), car.model)

    def test_create_driver_wtih_license_number(self):
        username = "Hiso"
        first_name = "Jimmy"
        last_name = "Likoswu"
        password = "testing1920"
        license_number = "KWQ12345"

        driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
