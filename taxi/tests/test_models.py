from django.contrib.auth import get_user_model

from django.test import TestCase

from taxi.models import Car, Manufacturer, Driver


class CarTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="test",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="first_test",
            last_name="last_test"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_assign_license(self):
        username = "test"
        password = "test12345"
        license_number = "QWE12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
