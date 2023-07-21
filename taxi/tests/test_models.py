from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class DriverModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(
            username="john_smith",
            license_number="ADM12345",
            first_name="John",
            last_name="Smith",
            password="Johns12345",
        )

    def test_driver_str(self):
        driver = Driver.objects.get(username="john_smith")

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_absolute_url(self):
        driver = Driver.objects.get(username="john_smith")
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.id}/")

    def test_create_driver_with_license_first_last_name(self):
        username = "jane_smith"
        license_number = "ADM12315"
        first_name = "Jane"
        last_name = "Smith"
        password = "Johns12345"
        driver = get_user_model().objects.create_user(
            username=username,
            license_number=license_number,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertTrue(driver.check_password(password))


class ManufacturerModelTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Citroen",
            country="France"
        )

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )


class CarModelTests(TestCase):

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Citroen",
            country="France"
        )
        car = Car.objects.create(
            model="C1",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), f"{car.model}")
