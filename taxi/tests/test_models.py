from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def test_manufacturer_format_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test country",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_format_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test country",
        )
        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), f"{car.model}")

    def test_driver_format_str(self):
        driver = Driver.objects.create_user(
            username="Test user",
            first_name="Test",
            last_name="Testovich",
            password="1qazcde3",
            license_number="QWE12345",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        username = "Test user"
        password = "1qazcde3"
        license_number = "QWE12345"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
