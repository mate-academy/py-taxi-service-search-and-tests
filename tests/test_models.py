from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Mercedes",
            country="Germany",
        )
        self.car = Car.objects.create(
            model="Gls",
            manufacturer=self.manufacturer,
        )
        self.driver = Driver.objects.create(
            username="test_user",
            first_name="John",
            last_name="Doe",
            license_number="ABC123"
        )
        self.car.drivers.add(self.driver)

    def test_manufacturer_str(self):
        self.assertEquals(str(self.manufacturer),
                          f"{self.manufacturer.name} "
                          f"{self.manufacturer.country}")

    def test_car_str(self):
        self.assertEquals(str(self.car), self.car.model)

    def test_driver_str(self):
        self.assertEquals(str(self.driver),
                          f"{self.driver.username} ({self.driver.first_name}"
                          f" {self.driver.last_name})")
