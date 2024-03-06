from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self) -> None:
        username = "admin"
        password = "1qazcde3"
        license_number = "JON26231"
        first_name = "Jon"
        last_name = "Doe"
        self.driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )

    def test_manufacturer_str_method(self):
        manufacturer = self.manufacturer
        self.assertEqual(str(manufacturer), "Audi Germany")

    def test_driver_str(self):
        driver = self.driver
        self.assertEqual(
            str(self.driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_create_author_with_lisence(self):
        driver = self.driver
        self.assertEqual(driver.license_number, "JON26231")

    def test_car_str_method(self):
        car = Car.objects.create(model="A6", manufacturer=self.manufacturer)
        self.assertEqual(str(car), "A6")
