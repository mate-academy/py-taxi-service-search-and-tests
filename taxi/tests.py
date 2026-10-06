
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicSearchTests(TestCase):
    def setUp(self):
        self.man1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.man2 = Manufacturer.objects.create(name="BMW", country="Germany")

        self.car1 = Car.objects.create(model="Camry", manufacturer=self.man1)
        self.car2 = Car.objects.create(model="X5", manufacturer=self.man2)

        self.driver1 = get_user_model().objects.create_user(
            username="john_doe",
            password="password123",
            license_number="LIC11111"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="jane_smith",
            password="password123",
            license_number="LIC22222"
        )

        self.client.force_login(self.driver1)

    def test_search_manufacturer_by_name(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "toy"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.man1, response.context["manufacturer_list"])
        self.assertNotIn(self.man2, response.context["manufacturer_list"])

    def test_search_car_by_model(self):
        response = self.client.get(CAR_URL, {"model": "x5"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.car2, response.context["car_list"])
        self.assertNotIn(self.car1, response.context["car_list"])

    def test_search_driver_by_username(self):
        response = self.client.get(DRIVER_URL, {"username": "jane"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.driver2, response.context["driver_list"])
        self.assertNotIn(self.driver1, response.context["driver_list"])

    def test_search_returns_all_if_query_is_empty(self):
        response = self.client.get(CAR_URL, {"model": ""})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 2)
