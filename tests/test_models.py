from django.test import TestCase

from taxi.models import Driver, Car, Manufacturer


class ModelsTests(TestCase):
    def test_driver_str_repr(self):
        driver = Driver.objects.create_user(
            username="Test",
            password="TestPassword123",
            email="email@example.com",
            first_name="John",
            last_name="Smith",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} {driver.last_name})")

    def test_car_str_repr(self):
        manufacturer = Manufacturer.objects.create(
            name="Test1",
            country="Country1"
        )
        car = Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer,
        )

        self.assertEqual(
            str(car),
            car.model
        )

    def test_manufacturer_str_repr(self):
        manufacturer = Manufacturer.objects.create(
            name="Test1",
            country="Country1"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )
