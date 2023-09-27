from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self) -> None:
        username = "admin"
        password = "1234wdfgh"
        license_number = "QWE78645"
        first_name = "qwe"
        last_name = "rty"
        self.driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Zhiga", country="Ukrain"
        )

    def test_manufacturer_str_method(self):
        manufacturer = self.manufacturer
        self.assertEqual(str(manufacturer), "Zhiga Ukrain")

    def test_driver_str(self):
        driver = self.driver
        self.assertEqual(
            str(self.driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_car_str_method(self):
        car = Car.objects.create(model="8", manufacturer=self.manufacturer)
        self.assertEqual(str(car), "8")

    def test_driver_create_with_license(self):
        driver = self.driver
        self.assertEqual(driver.license_number, "QWE78645")
