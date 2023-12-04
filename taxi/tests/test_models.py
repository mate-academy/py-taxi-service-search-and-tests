from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import (
    Manufacturer,
    Car, Driver,
)


class ModelTests(TestCase):
    USER_PASSWORD = "KoLd(884%1"

    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="Terry111999",
            first_name="Terry",
            last_name="Richardson",
            license_number="MIK25131",
            password=cls.USER_PASSWORD
        )

    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Cybulya", country="Ukraine"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}",
        )

    def test_car_str(self) -> None:
        car_model_test = "L17"
        driver_test = Driver.objects.get(id=1)
        manufacturer_test = Manufacturer.objects.create(
            name="Cybulya", country="Ukraine"
        )
        car_test = Car.objects.create(
            model=car_model_test,
            manufacturer=manufacturer_test,
        )
        car_test.drivers.add(driver_test)
        self.assertEqual(str(car_test), car_test.model)

    def test_driver_str(self) -> None:
        driver_test = Driver.objects.get(id=1)

        self.assertEqual(
            str(driver_test),
            f"{driver_test.username} "
            f"({driver_test.first_name} {driver_test.last_name})",
        )

    def test_driver_license_number(self) -> None:
        driver_test = Driver.objects.get(id=1)
        self.assertEqual(
            str(driver_test.license_number),
            driver_test.license_number
        )

    def test_driver_password(self) -> None:
        driver_test = Driver.objects.get(id=1)
        self.assertTrue(driver_test.check_password(self.USER_PASSWORD))
