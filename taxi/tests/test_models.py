from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="dirvertest",
            first_name="First",
            last_name="Lasts",
            license_number="CAD25252",
            password="drivepass22",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="TestBrand",
            country="TestCountry",
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self) -> None:
        car = Car.objects.create(
            model="TestMOdel",
            manufacturer=Manufacturer.objects.create(
                name="TestBrand",
                country="TestCountry"
            ),
        )

        self.assertEqual(str(car), car.model)
