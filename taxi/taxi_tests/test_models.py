from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        self.driver = get_user_model().objects.create(
            username="driver",
            password="test123",
            first_name="Driver1",
            last_name="Driver2",
            license_number="XYZ12345",
        )

        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer,
        )

        self.car.drivers.add(self.driver)

    def test_manufacturer_str(self):
        expected_str = f"{self.manufacturer.name} {self.manufacturer.country}"
        self.assertEqual(str(self.manufacturer), expected_str)

    def test_driver_str(self):
        expected_str = (f""
                        f"{self.driver.username}"
                        f" ({self.driver.first_name}"
                        f" {self.driver.last_name})"
                        )
        self.assertEqual(str(self.driver), expected_str)

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_driver_get_absolute_url(self):
        expected_url = f"/drivers/{self.driver.pk}/"
        self.assertEqual(str(self.driver.get_absolute_url()), expected_url)

    def test_car_relations(self):
        self.assertEqual(self.car.manufacturer.name, "Toyota")
        self.assertIn(self.driver, self.car.drivers.all())
        self.assertIn(self.car, self.driver.cars.all())
