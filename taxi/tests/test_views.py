from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.models import Car, Manufacturer, Driver

User = get_user_model()

class CarViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        self.manufacturer = Manufacturer.objects.create(name="Audi", country="Germany")
        self.car = Car.objects.create(model="A6", manufacturer=self.manufacturer)

    def test_car_list_view(self):
        """Перевіряємо, чи доступний список автомобілів"""
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A6")

    def test_car_detail_view(self):
        """Перевіряємо, чи доступна детальна сторінка авто"""
        response = self.client.get(reverse("taxi:car-detail", args=[self.car.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A6")


class DriverViewTest(TestCase):
    def setUp(self):
        self.driver = User.objects.create_user(username="driver1", password="pass123", license_number="XYZ12345")
        self.client.login(username="driver1", password="pass123")

    def test_driver_list_view(self):
        """Перевіряємо, чи доступний список водіїв"""
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")

    def test_driver_detail_view(self):
        """Перевіряємо, чи доступна детальна сторінка водія"""
        response = self.client.get(reverse("taxi:driver-detail", args=[self.driver.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "XYZ12345")
