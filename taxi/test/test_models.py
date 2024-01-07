from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


# Create your tests here.
class Modelstests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(name="test")
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create(
            username="test",
            password="12345",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(str(driver),
                         f"{driver.username}"
                         f" ({driver.first_name}"
                         f" {driver.last_name})")

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(name="test")
        car = Car.objects.create(model="X5", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_driver_license_number(self) -> None:
        username = "test"
        license_number = "ACV12345"
        password = "12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name="test_first",
            last_name="test_last",
            license_number=license_number
        )
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
