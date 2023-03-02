from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="test_name",
            password="User12345",
            first_name="test_first",
            last_name="test_last",
            license_number="TES12345",
        )

        self.assertTrue(driver.license_number == "TES12345")
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer
        )

        self.assertEqual(str(car), car.model)
