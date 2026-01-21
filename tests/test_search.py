from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(username="john_doe",
                                             license_number="ABC12345")
        self.driver2 = Driver.objects.create(username="jane_smith",
                                             license_number="XYZ67890")

        self.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan")

        self.car1 = Car.objects.create(model="Camry",
                                       manufacturer=self.manufacturer)
        self.car2 = Car.objects.create(model="Corolla",
                                       manufacturer=self.manufacturer)

    def test_driver_search(self):
        response = self.client.get(reverse("taxi:driver-list") + "?q=john")
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "jane_smith")

    def test_car_search(self):
        response = self.client.get(reverse("taxi:car-list") + "?q=Camry")
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Corolla")

    def test_manufacturer_search(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list") + "?q=Toyota")
        self.assertContains(response, "Toyota")
