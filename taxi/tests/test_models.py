from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="olesshulzh",
            password="2405",
            first_name="Oles",
            last_name="Shulzhenko"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        car = Car.objects.create(model="Q8", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_create_driver_width_license_number(self):
        username = "olesshulzh"
        password = "2405"
        license_number = "OSh240596"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(str(driver.username), username)
        self.assertEqual(str(driver.license_number), license_number)
        self.assertTrue(driver.check_password(password))
