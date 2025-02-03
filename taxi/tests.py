from django.test import TestCase
from django.urls import reverse
from .models import Driver, Car, Manufacturer

class DriverSearchTest(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(username="testdriver")
        self.driver2 = Driver.objects.create(username="anotherdriver")

    def test_search_driver_by_username(self):
        response = self.client.get(reverse("driver_list") + "?q=test")
        self.assertContains(response, "testdriver")
        self.assertNotContains(response, "anotherdriver")

class CarSearchTest(TestCase):
    def setUp(self):
        self.car1 = Car.objects.create(model="Toyota")
        self.car2 = Car.objects.create(model="BMW")

    def test_search_car_by_model(self):
        response = self.client.get(reverse("car_list") + "?q=Toyota")
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(name="Tesla")
        self.manufacturer2 = Manufacturer.objects.create(name="Ford")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(reverse("manufacturer_list") + "?q=Tesla")
        self.assertContains(response, "Tesla")
        self.assertNotContains(response, "Ford")
