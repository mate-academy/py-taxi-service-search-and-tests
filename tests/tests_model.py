from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username='test',
            password='<PASSWORD>',
            first_name="Troll",
            last_name="Darken",
            license_number="123456",
        )

    def test_str(self):
        self.assertEqual(str(self.driver), "test (Troll Darken)")


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )

    def test_str(self):
        self.assertEqual(str(self.manufacturer), "BMW Germany")




class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        self.car = Car.objects.create(
            model="M5", manufacturer=self.manufacturer
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), "M5")

    def test_car_manufacturer_relationship(self):
        self.assertEqual(self.car.manufacturer, self.manufacturer)
