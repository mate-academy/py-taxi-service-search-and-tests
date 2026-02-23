from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTest(TestCase):
    def test_manufacturer_format_str(self) -> None:
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        self.assertEquals(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_format_str(self) -> None:
        driver = Driver.objects.create(
            username="test",
            license_number="ABC12345",
            first_name="Max",
            last_name="Lesyk"
        )
        self.assertEquals(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_format_str(self) -> None:
        driver = Driver.objects.create(
            username="test",
            license_number="ABC12345",
            first_name="Max",
            last_name="Lesyk"
        )
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )
        car.drivers.add(driver)
        self.assertEquals(str(car), car.model)

    def test_create_driver(self) -> None:
        username = "test"
        license_number = "ABC12345"
        first_name = "Max"
        last_name = "Lesyk"
        password = "test123"
        driver = Driver.objects.create_user(
            username=username,
            license_number=license_number,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        self.assertEquals(driver.username, username)
        self.assertEquals(driver.license_number, license_number)
        self.assertEquals(driver.first_name, first_name)
        self.assertEquals(driver.last_name, last_name)
        self.assertTrue(driver.check_password(password))
