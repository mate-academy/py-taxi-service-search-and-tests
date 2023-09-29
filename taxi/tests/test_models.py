from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Mazda",
            country="Japan"
        )
        self.assertEquals(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create(
            username="Homer_S",
            password="Springfield",
            first_name="Homer",
            last_name="Simson",
            license_number="ABC12345"
        )
        self.assertEquals(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_license_number(self) -> None:
        driver = get_user_model().objects.create(
            username="Homer_S",
            password="Springfield",
            first_name="Homer",
            last_name="Simson",
            license_number="ABC12345"
        )
        self.assertEquals(driver.license_number, "ABC12345")

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Mazda",
            country="Japan"
        )
        car = Car.objects.create(
            model="RX-Vision",
            manufacturer=manufacturer,
        )
        self.assertEquals(str(car), car.model)
