from django.test import TestCase
from django.urls import reverse
from .models import Driver, Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(username="testuser1")
        self.driver2 = Driver.objects.create(username="testuser2")
        self.car1 = Car.objects.create(model="Test Model 1")
        self.car2 = Car.objects.create(model="Test Model 2")
        self.manufacturer1 = Manufacturer.objects.create(
            name="Test Manufacturer 1")
        self.manufacturer2 = Manufacturer.objects.create(
            name="Test Manufacturer 2")

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-search") + "?q=testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser1")
        self.assertNotContains(response, "testuser2")

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-search") + "?q=Test Model 1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Model 1")
        self.assertNotContains(response, "Test Model 2")

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-search") + "?q=Test Manufacturer 1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Manufacturer 1")
        self.assertNotContains(response, "Test Manufacturer 2")
