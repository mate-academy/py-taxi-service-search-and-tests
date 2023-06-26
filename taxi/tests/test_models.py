from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(name="test", country="test")

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} " f"{manufacturer.country}",
        )

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(name="test", country="test")

        car = Car.objects.create(model="TestCar", manufacturer=manufacturer)

        self.assertEqual(str(car), f"{car.model}")

    def test_create_driver_with_license(self) -> None:
        username = "Red John"
        password = "test12345"
        first_name = "John"
        last_name = "Doe"
        license_number = "SEB97856"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="PatrickJane",
            password="test12345",
            first_name="Patrick",
            last_name="Jane",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} "
            f"{driver.last_name})",
        )
