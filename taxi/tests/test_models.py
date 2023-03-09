from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_create_driver_with_license_number(self) -> None:
        username = "test"
        password = "Test1234"
        license_number = "TES12345"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_car_str(self) -> None:
        model = "test"
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
