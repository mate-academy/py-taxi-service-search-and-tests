from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name = "BMW",
            country="Germany"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="admin.user",
            password="qwe12345",
            first_name="Admin",
            last_name="last_admin"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_drive_license(self):
        username = "admin.user"
        password = "qwe12345"
        license_number = "qwe12345"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        car = Car.objects.create(
            model="EQS",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), car.model)
