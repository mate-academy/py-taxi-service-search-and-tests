from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Car, Manufacturer, Driver

class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password123"
        )
        self.driver1 = Driver.objects.create_user(
            username="driver1",
            password="password123",
            first_name="John",
            last_name="Doe",
            license_number="12345ABC"
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2",
            password="password123",
            first_name="Jane",
            last_name="Doe",
            license_number="67890XYZ"
        )

    def test_driver_search_by_first_name(self):
        self.client.login(username="user", password="password123")
        response = self.client.get(reverse("taxi:driver-list"), {"search": "John"})
        self.assertContains(response, "John")
        self.assertNotContains(response, "Jane")

    def test_driver_search_by_last_name(self):
        self.client.login(username="user", password="password123")
        response = self.client.get(reverse("taxi:driver-list"), {"search": "Doe"})
        self.assertContains(response, "Doe")
        self.assertNotContains(response, "Jane")

    def test_driver_search_by_license_number(self):
        self.client.login(username="user", password="password123")
        response = self.client.get(reverse("taxi:driver-list"), {"search": "12345ABC"})
        self.assertContains(response, "12345ABC")
        self.assertNotContains(response, "Jane")


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password123"
        )
        manufacturer = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.car1 = Car.objects.create(model="Camry", manufacturer=manufacturer)
        self.car2 = Car.objects.create(model="Corolla", manufacturer=manufacturer)

    def test_car_search_by_model(self):
        self.client.login(username="user", password="password123")
        response = self.client.get(reverse("taxi:car-list"), {"search": "Camry"})
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Corolla")

    def test_car_search_by_manufacturer(self):
        self.client.login(username="user", password="password123")
        response = self.client.get(reverse("taxi:car-list"), {"manufacturer": "Toyota"})
        self.assertContains(response, "Camry")
        self.assertContains(response, "Corolla")


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password123"
        )
        self.manufacturer1 = Manufacturer.objects.create(name="BMW", country="Germany")
        self.manufacturer2 = Manufacturer.objects.create(name="Toyota", country="Japan")

    def test_manufacturer_search_by_name(self):
        self.client.login(username="user", password="password123")
        response = self.client.get(reverse("taxi:manufacturer-list"), {"search": "BMW"})
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Toyota")

    def test_manufacturer_search_by_country(self):
        self.client.login(username="user", password="password123")
        response = self.client.get(reverse("taxi:manufacturer-list"), {"search": "Germany"})
        self.assertNotContains(response, "BMW")
        self.assertNotContains(response, "Toyota")
