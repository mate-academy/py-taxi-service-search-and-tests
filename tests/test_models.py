from django.test import TestCase

from taxi.models import Driver, Car, Manufacturer


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="manufacturer_name",
            country="manufacturer_country"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="driver_username",
            first_name="driver_first_name",
            last_name="driver_last_name",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="car_model",
            manufacturer=self.manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )
