from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car

CARS_LIST_URL = reverse("taxi:car-list")


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.login(username="testuser", password="password")

        self.manufacturer1 = Manufacturer.objects.create(name="Toyota")
        self.manufacturer2 = Manufacturer.objects.create(name="Ford")

        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Mustang",
            manufacturer=self.manufacturer2
        )
        self.car3 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1
        )

    def test_search_no_query(self):
        response = self.client.get(CARS_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertContains(response, "Mustang")
        self.assertContains(response, "Corolla")

    def test_search_with_query(self):
        response = self.client.get(CARS_LIST_URL, {"model": "camry"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Mustang")
        self.assertNotContains(response, "Corolla")

    def test_search_with_partial_match_query(self):
        response = self.client.get(CARS_LIST_URL, {"model": "rol"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Camry")
        self.assertNotContains(response, "Mustang")

    def test_search_with_no_results(self):
        response = self.client.get(CARS_LIST_URL, {"model": "nonexistent"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Camry")
        self.assertNotContains(response, "Mustang")
        self.assertNotContains(response, "Corolla")
