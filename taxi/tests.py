from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class SearchFeatureTests(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota", country="Japan")
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford", country="USA")
        self.car1 = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer1)
        self.car2 = Car.objects.create(
            model="Mustang", manufacturer=self.manufacturer2)
        self.driver1 = Driver.objects.create_user(
            username="john_doe", password="password123",
            license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="jane_doe", password="password123",
            license_number="XYZ67890"
        )

        self.client.login(username="john_doe", password="password123")

    def test_search_manufacturer(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"q": "Toyota"})
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_search_car(self):
        response = self.client.get(reverse("taxi:car-list"), {"q": "Camry"})
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Mustang")

    def test_search_driver(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"q": "john_doe"})
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "jane_doe")
