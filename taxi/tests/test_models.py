from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class StringModelsTest(TestCase):
    def test_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver(self):
        driver = Driver.objects.create_user(
            username="Test",
            first_name="Test",
            last_name="Test",
            password="Test123",
            license_number="TST12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test country"
        )

        car = Car.objects.create(
            model="TS1",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
