from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Name", country="Country"
        )
        f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="test.user",
            first_name="Firstname",
            last_name="Lastname"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        Manufacturer.objects.create(
            name="Test Name", country="Country"
        )
        car = Car.objects.create(model="Test Model", manufacturer_id=1)
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test.user"
        password = "pass321"
        license_number = "XYZ12345"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
