from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car
from django.contrib.auth import get_user_model


User = get_user_model()


class SearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC54321",
        )
        self.client.login(username="testuser", password="testpass123")

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer2
        )

        self.driver1 = User.objects.create_user(
            username="driver1",
            password="testpass123",
            license_number="DFG12345"
        )
        self.driver2 = User.objects.create_user(
            username="john_doe",
            password="testpass123",
            license_number="XYZ54321"
        )

    def test_manufacturer_search(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_car_search(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "Corolla"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Focus")

    def test_driver_search(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "john"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "driver1")
