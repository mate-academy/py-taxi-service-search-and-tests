from django.test import TestCase
from .models import Driver, Car, Manufacturer


class SearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver1 = Driver.objects.create(username="john_doe",
                                            license_number="LICENSE123")
        cls.driver2 = Driver.objects.create(username="jane_doe",
                                            license_number="LICENSE456")
        cls.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                       country="Japan")
        cls.car1 = Car.objects.create(model="Camry",
                                      manufacturer=cls.manufacturer)

    def test_driver_search(self):
        response = self.client.get("/search/drivers/?q=john")
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "jane_doe")

    def test_car_search(self):
        response = self.client.get("/search/cars/?q=Camry")
        self.assertContains(response, "Camry")

    def test_manufacturer_search(self):
        response = self.client.get("/search/manufacturers/?q=Toyota")
        self.assertContains(response, "Toyota")
