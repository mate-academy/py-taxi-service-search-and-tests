from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class SearchViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test.user",
            password="password123",
            license_number="TST12345",
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )

        self.driver1 = get_user_model().objects.create_user(
            username="john_doe",
            password="password123",
            license_number="ABC12345",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="alice_smith",
            password="password123",
            license_number="XYZ67890",
        )

        self.car1 = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Model S", manufacturer=self.manufacturer2
        )

    def test_search_car_by_model(self):
        response = self.client.get(CAR_LIST_URL, {"model": "Cam"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.car1, response.context["car_list"])
        self.assertNotIn(self.car2, response.context["car_list"])

    def test_search_driver_by_username(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "john"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.driver1, response.context["driver_list"])
        self.assertNotIn(self.driver2, response.context["driver_list"])

    def test_search_manufacturer_by_name(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "Toy"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            self.manufacturer1, response.context["manufacturer_list"]
        )
        self.assertNotIn(
            self.manufacturer2, response.context["manufacturer_list"]
        )
