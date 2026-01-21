from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver

class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("taxi:manufacturer-list") # Ensure URL name matches your urls.py
        self.factory1 = Manufacturer.objects.create(name="Tesla", country="USA")
        self.factory2 = Manufacturer.objects.create(name="Toyota", country="Japan")

    def test_search_manufacturer_by_name(self):
        # Test searching for 'Tesla'
        response = self.client.get(self.url, {"search_query": "Tes"})
        self.assertEqual(response.status_code, 200)
        
        # Check if Tesla is in the context/content
        self.assertContains(response, self.factory1.name)
        
        # Check if Toyota is NOT in the context/content
        self.assertNotContains(response, self.factory2.name)

    def test_search_manufacturer_no_result(self):
        response = self.client.get(self.url, {"search_query": "Ford"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.factory1.name)
        self.assertNotContains(response, self.factory2.name)

class CarSearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("taxi:car-list")
        self.manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        self.driver = Driver.objects.create(username="testdriver", password="password")
        
        self.car1 = Car.objects.create(model="Model S", manufacturer=self.manufacturer)
        self.car2 = Car.objects.create(model="Model X", manufacturer=self.manufacturer)
        self.car3 = Car.objects.create(model="Camry", manufacturer=self.manufacturer)

    def test_search_car_by_model(self):
        # Search specifically for 'Model' (should find S and X, but not Camry)
        response = self.client.get(self.url, {"search_query": "Model"})
        
        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)
        self.assertNotContains(response, self.car3.model)

class DriverSearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("taxi:driver-list")
        self.driver1 = Driver.objects.create_user(username="alice", password="123")
        self.driver2 = Driver.objects.create_user(username="bob", password="123")

    def test_search_driver_by_username(self):
        response = self.client.get(self.url, {"search_query": "ali"})
        
        self.assertContains(response, "alice")
        self.assertNotContains(response, "bob")
