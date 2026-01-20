from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver
from django.contrib.auth import get_user_model


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Tesla", country="USA")

    def test_manufacturer_search(self):
        response = self.client.get(reverse("taxi:manufacturer-list"), {"name": "Toyota"})
        self.assertEqual(response.status_code, 200)  # Проверяем, что ответ успешный
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Tesla")

    def test_manufacturer_list_all(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Tesla")


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        Car.objects.create(model="Model S", manufacturer=manufacturer)
        Car.objects.create(model="Model X", manufacturer=manufacturer)

    def test_car_search(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "Model S"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model S")
        self.assertNotContains(response, "Model X")

    def test_car_list_all(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model S")
        self.assertContains(response, "Model X")


class DriverSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        Driver.objects.create_user(username="testuser1", password="password123", license_number="ABC12345")
        Driver.objects.create_user(username="anotheruser", password="password123", license_number="XYZ67890")

    def test_driver_search(self):
        response = self.client.get(reverse("taxi:driver-list"), {"username": "testuser1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser1")
        self.assertNotContains(response, "anotheruser")

    def test_driver_list_all(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser1")
        self.assertContains(response, "anotheruser")
