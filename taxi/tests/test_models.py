from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.assertEqual(str(manufacturer), "BMW Germany")


class CarModelTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        car = Car.objects.create(
            model="X5",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), "X5")
