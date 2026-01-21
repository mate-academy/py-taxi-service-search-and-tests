from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.name = "BMW"
        self.country = "Germany"
        self.manufacturer = Manufacturer.objects.create(
            name=self.name,
            country=self.country
        )

    def test_manufacturer_str(self) -> None:
        self.assertEqual(
            str(self.manufacturer),
            f"{self.name} {self.country}"
        )

    def test_driver_str(self) -> None:
        driver = Driver.objects.create(
            username="ErenJaeger",
            first_name="Eren",
            last_name="Jaeger",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self) -> None:
        model = "BMW x4"
        car = Car.objects.create(
            model=model,
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), model)
