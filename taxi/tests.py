from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="testuser",
            password="password",
            license_number="LIC00000"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )

    def test_driver_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")

    def test_car_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Corolla"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Toyota"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
