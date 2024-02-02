from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Mazda",
            country="Japan"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Mazda",
            country="Japan"
        )
        car = Car.objects.create(
            model="CX-3",
            manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_drink_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="testpass",
            first_name="test first",
            last_name="test last"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_have_license_number(self):
        license_number = "AAA11111"
        driver = get_user_model().objects.create_user(
            username="test",
            password="testpass",
            first_name="test first",
            last_name="test last",
            license_number=license_number
        )
        self.assertEqual(driver.license_number, license_number)
