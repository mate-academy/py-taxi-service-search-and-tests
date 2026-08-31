from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver

class PublicTaxiSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_search(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")
    
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Toyota"}
        )
        self.assertEqual(response.status_code, 200)

    def test_car_list_search(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        Car.objects.create(model="X5", manufacturer=manufacturer)
    
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Corolla"}
        )
        self.assertEqual(response.status_code, 200)

    def test_driver_list_search(self):
        Driver.objects.create_user(username="johndoe", password="password123", license_number="ABC12345")
        Driver.objects.create_user(username="janedoe", password="password123", license_number="XYZ98765")
    
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "johndoe"}
        )
        self.assertEqual(response.status_code, 200)
