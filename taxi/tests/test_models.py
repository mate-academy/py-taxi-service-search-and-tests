from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="Test username",
            first_name="Test first_name",
            last_name="Test last_name",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )

        car = Car.objects.create(
            model="Test_model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)
