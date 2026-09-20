from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(name="Test", country="Test")
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_car_str(self) -> None:
        test_manufacturer = Manufacturer.objects.create(name="Test",
                                                        country="Test")
        car = Car.objects.create(model="Test1", manufacturer=test_manufacturer)
        self.assertEqual(str(car), car.model)

    def test_driver_str(self) -> None:
        test_user = get_user_model().objects.create_user(
            username="Test",
            first_name="Test first",
            last_name="Test first",
            password="test_password"
        )
        self.assertEqual(
            str(test_user),
            f"{test_user.username} "
            f"({test_user.first_name} {test_user.last_name})"
        )

    def test_driver_license(self) -> None:
        username = "Test"
        password = "Test_password"
        license_number = "ABC18185"
        user = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.license_number, license_number)
