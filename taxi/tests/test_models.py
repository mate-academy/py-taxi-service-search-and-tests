from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="name",
            country="country"
        )

        self.driver = get_user_model().objects.create(
            username="user",
            password="test555",
            first_name="Tom",
            last_name="Brain"
        )
        self.car = Car.objects.create(
            model="model_test",
            manufacturer=self.manufacturer,
        )

    def test_manufacturer_str(self) -> None:
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_car_str(self) -> None:
        self.assertEqual(str(self.car), self.car.model)

    def test_driver_str(self) -> None:
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_driver_license(self):
        username = "driver"
        password = "license"
        license_number = "ABC99999"
        driver = get_user_model().objects.create(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.password, password)
        self.assertEqual(driver.license_number, license_number)
