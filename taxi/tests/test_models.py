from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test",
                                                   country="UA")
        self.assertEqual(str(manufacturer), "test UA")

    def test_driver_str(self):
        driver = Driver.objects.create(username="test",
                                       password="12345",
                                       first_name="test first",
                                       last_name="test last",
                                       license_number="UA12345")
        self.assertEqual(str(driver), "test (test first test last)")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test",
                                                   country="UA")
        car = Car.objects.create(model="test",
                                 manufacturer=manufacturer)
        self.assertEqual(str(car), "test")
