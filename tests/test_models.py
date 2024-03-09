from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ManufacturerTest(TestCase):
    def test_manufacturer_str_method(self) -> None:
        manufacture = Manufacturer.objects.create(
            name="test",
            country="USA"
        )

        self.assertEqual(str(manufacture), "test USA")


class DriverTest(TestCase):
    def test_driver_str_method(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test_username",
            password="test123",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="AAA55555"
        )

        self.assertEqual(
            str(driver),
            "test_username (test_first_name test_last_name)"
        )

    def test_driver_get_absolute_url_method(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test_username",
            password="test123",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="AAA55555"
        )

        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_create_driver_with_license_number(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test_username",
            password="test123",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="AAA55555"
        )

        self.assertEqual(driver.license_number, "AAA55555")
        self.assertEqual(driver.username, "test_username")
        self.assertTrue(driver.check_password("test123"))


class CarTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )

    def test_car_str_method(self) -> None:
        car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )

        self.assertEqual(str(car), "test_model")
