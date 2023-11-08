from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create(
            username="test",
            first_name="test1",
            last_name="test2",
            password="test123"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345",
        )
        self.assertEqual(driver.username, "test")
        self.assertEqual(driver.license_number, "ABC12345")
        self.assertTrue(driver.check_password("test123"))

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        driver = get_user_model().objects.create(
            username="test",
            first_name="test1",
            last_name="test2",
            password="test123"
        )
        car = Car.objects.create(
            model="test_car",
            manufacturer=manufacturer
        )
        car.drivers.set([driver])

        self.assertEqual(
            str(car), car.model
        )
