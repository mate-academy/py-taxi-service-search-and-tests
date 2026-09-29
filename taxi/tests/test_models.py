from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test country"
        )
        cls.driver = Driver.objects.create(
            username="test123",
            first_name="test",
            last_name="testovich"
        )
        cls.car = Car.objects.create(
            model="testmodel",
            manufacturer=cls.manufacturer
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "test test country")

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "test123 (test testovich)")

    def test_driver_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            f"/drivers/{self.driver.pk}/"
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), "testmodel")
