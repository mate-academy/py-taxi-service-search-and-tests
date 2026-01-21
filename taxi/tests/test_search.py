from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer
from django.contrib.auth import get_user_model
User = get_user_model()


class SearchTests(TestCase):
    def setUp(self):
        # створюємо тестові дані
        self.driver1 = User.objects.create_user(
            username="john",
            password="12345",
            license_number="ABC12345"
        )
        self.driver2 = User.objects.create_user(
            username="mike",
            password="12345",
            license_number="XYZ98765"
        )

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan")
        self.manufacturer2 = Manufacturer.objects.create(
            name="Tesla",
            country="USA")

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1)
        self.car2 = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer2)

        self.client.force_login(self.driver1)

    def test_search_driver_by_username(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "john"})

        self.assertIn(self.driver1, response.context["driver_list"])
        self.assertNotIn(self.driver2, response.context["driver_list"])

    def test_search_car_by_model(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "Corolla"})

        self.assertIn(self.car1, response.context["car_list"])
        self.assertNotIn(self.car2, response.context["car_list"])

    def test_search_car_no_results(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "DoesNotExist"})
        self.assertEqual(len(response.context["car_list"]), 0)

    def test_search_manufacturer_by_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Tesla"})

        self.assertIn(
            self.manufacturer2,
            response.context["manufacturer_list"])
        self.assertNotIn(
            self.manufacturer1,
            response.context["manufacturer_list"])

    def test_search_manufacturer_no_results(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Unknown"})
        self.assertEqual(len(response.context["manufacturer_list"]), 0)

    def test_search_no_results(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "unknown"})
        self.assertEqual(len(response.context["driver_list"]), 0)
