from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.test import TestCase

from ..models import Manufacturer, Car


class ManufacturerModelTest(TestCase):

    def test_manufacturer_str(self) -> None:
        test_manufacturer = Manufacturer.objects.create(
            name="<NAME>", country="<COUNTRY>"
        )

        self.assertEqual(
            str(test_manufacturer),
            f"{test_manufacturer.name} {test_manufacturer.country}"
        )


class CarModelTest(TestCase):

    def test_car_str(self) -> None:
        test_manufacturer = Manufacturer.objects.create(
            name="<NAME>", country="<COUNTRY>"
        )

        test_car = Car.objects.create(
            model="<MODEL>", manufacturer=test_manufacturer
        )

        self.assertEqual(
            str(test_car),
            test_car.model
        )


class DriverModelTest(TestCase):

    @staticmethod
    def create_user() -> AbstractUser:
        test_driver = get_user_model().objects.create(
            username="<NAME>", first_name="<NAME>", last_name="<NAME>",
            password="<PASSWORD>"
        )

        return test_driver

    def test_driver_str(self) -> None:
        test_driver = self.create_user()

        self.assertEqual(
            str(test_driver),
            f"{test_driver.username} ({test_driver.first_name} {test_driver.last_name})"
        )

    def test_driver_license_number(self) -> None:
        license_number = "AAA33333"

        test_driver = self.create_user()
        test_driver.license_number = license_number
        test_driver.save()

        self.assertEqual(
            test_driver.license_number,
            license_number
        )
