from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        self.driver = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
        )

    def test_manufacturer_str(self) -> None:
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_car_str(self) -> None:
        car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        car.drivers.set([self.driver])
        self.assertEqual(str(car), car.model)

    def test_car_with_multiple_drivers(self) -> None:
        driver2 = get_user_model().objects.create(
            username="test2",
            password="test1234",
            first_name="test2_first",
            last_name="test2_last",
            license_number="test_license_2",
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        car.drivers.set([self.driver, driver2])
        self.assertEqual(car.drivers.count(), 2)
        self.assertIn(self.driver, car.drivers.all())
        self.assertIn(driver2, car.drivers.all())

    def test_driver_with_license_number(self) -> None:
        username = "test_username"
        password = "test_123"
        license_number = "test_license_number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
