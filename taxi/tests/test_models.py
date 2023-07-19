from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Car, Driver, Manufacturer


class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="BMW", country="Germany")
        get_user_model().objects.create_user(
            username="Test",
            password="Test12345",
            first_name="FirstName",
            last_name="LastName",
            license_number="TRE12345",
        )
        Car.objects.create(
            model="X5", manufacturer=Manufacturer.objects.get(id=1)
        )

    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.get(id=1)
        info = f"{manufacturer.name} {manufacturer.country}"

        self.assertEqual(str(manufacturer), info)

    def test_car_str(self) -> None:
        car = Car.objects.get(id=1)

        self.assertEqual(str(car), car.model)

    def test_driver_str(self) -> None:
        driver = Driver.objects.get(id=1)

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_creating_driver_with_lisence(self) -> None:
        driver = Driver.objects.get(id=1)

        self.assertEqual(driver.license_number, "TRE12345")

    def test_driver_get_absolute_url(self) -> None:
        driver = Driver.objects.get(id=1)

        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")
