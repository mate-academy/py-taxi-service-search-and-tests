from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="BMW", country="Germany")
        self.driver = Driver.objects.create(
            username="test",
            first_name="John",
            last_name="Wick",
            license_number="MIK25135"
        )
        self.car = Car.objects.create(model="Camry", manufacturer=self.manufacturer)

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), f"{self.manufacturer.name} {self.manufacturer.country}")

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} ({self.driver.first_name} {self.driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), f"/drivers/{self.driver.pk}/")

    def test_car_str(self):
        self.assertEqual(str(self.car), "Camry")
