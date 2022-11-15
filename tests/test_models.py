from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelsTest(TestCase):
    def test_car_str(self):
        car = Car.objects.create(
            model="test",
            manufacturer=Manufacturer.objects.create(
                name="test", country="test"
            ),
        )
        self.assertEqual(str(car), car.model)

    def test_driver_dtr(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last",
            license_number="Test last",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_with_license_number(self):
        password = "test12345"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username="test",
            first_name="testname",
            last_name="testsurname",
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, "test")
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password), password)
