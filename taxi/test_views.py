from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Manufacturer, Car

User = get_user_model()


class TestSearchViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="ana",
            password="password",
            license_number="L123",
        )
        self.other_driver = User.objects.create_user(
            username="bruno",
            password="password",
            license_number="L456",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer,
        )

    def test_driver_search(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "ana"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ana")
        self.assertNotContains(response, "bruno")

    def test_manufacturer_search(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toyo"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")

    def test_car_search_and_empty_query(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Cor"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        response_empty = self.client.get(
            reverse("taxi:car-list"),
            {"model": ""},
        )
        self.assertEqual(response_empty.status_code, 200)
        self.assertContains(response_empty, "Corolla")
