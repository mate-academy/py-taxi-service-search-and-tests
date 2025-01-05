from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="test",
            password="test123",
            first_name="Jhon",
            last_name="Doe",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")

        car = Car.objects.create(model="test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license(self):

        username = "test"
        password = "test123"
        license_number = "ABC12345"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
