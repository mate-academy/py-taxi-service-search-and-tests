from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

    def test_manufacturer_str(self) -> None:
        self.assertEquals(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_car_str(self) -> None:
        car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer
        )
        self.assertEquals(
            str(car),
            car.model)

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create(
            username="awesome_username",
            first_name="awesome_name",
            last_name="last_name",
            password="strongestPassword",
            license_number="ABC12345"
        )
        self.assertEquals(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})")
