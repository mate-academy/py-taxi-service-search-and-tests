from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Mazda", country="Japan"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} "
            f"{manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="testuser",
            first_name="User",
            last_name="Test",
            license_number="DVS12345",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} "
            f"{driver.last_name})",
        )

    def test_create_user_with_license_number(self) -> None:
        username = "User"
        password = "passforuser12345"
        license_number = "DFF12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password), password)
        self.assertEqual(driver.license_number, license_number)

    def test_car_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="testuser",
            first_name="User",
            last_name="Test",
            license_number="DVS12345",
        )
        manufacturer = Manufacturer.objects.create(
            name="Mazda",
            country="Japan"
        )
        car = Car.objects.create(
            model="CX-5",
            manufacturer=manufacturer
        )
        car.drivers.add(driver)
        self.assertEqual(str(car), car.model)
