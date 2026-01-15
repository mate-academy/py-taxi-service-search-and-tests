from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer


class DriverSearchTest(TestCase):
    def setUp(self):
        user = get_user_model()
        self.driver1 = user.objects.create_user(
            username="alex", password="pass123"
        )
        self.driver2 = user.objects.create_user(
            username="maria", password="pass123"
        )
        self.client.force_login(self.driver1)

    def test_search_no_query_returns_all(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertContains(response, "alex")
        self.assertContains(response, "maria")

    def test_search_query_matches_one(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"query": "alex"}
        )
        self.assertContains(response, "alex")
        self.assertNotContains(response, "maria")

    def test_search_query_no_match(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"query": "zzz"}
        )
        self.assertNotContains(response, "alex")
        self.assertNotContains(response, "maria")


class CarSearchTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Testland"
        )
        self.car1 = Car.objects.create(
            model="BMW",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="mers",
            manufacturer=self.manufacturer
        )

    def test_search_no_query_returns_all(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertContains(response, "bmw")
        self.assertContains(response, "mers")

    def test_search_query_matches_one(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"query": "bmw"}
        )
        self.assertContains(response, "bmw")
        self.assertNotContains(response, "mers")

    def test_search_query_no_match(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"query": "zzz"}
        )
        self.assertNotContains(response, "bmw")
        self.assertNotContains(response, "mers")


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(
            name="alex",
            country="Testland"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="maria",
            country="Testland2"
        )

    def test_search_no_query_returns_all(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertContains(response, "alex")
        self.assertContains(response, "maria")

    def test_search_query_matches_one(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"query": "alex"}
        )
        self.assertContains(response, "alex")
        self.assertNotContains(response, "maria")

    def test_search_query_no_match(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"query": "zzz"}
        )
        self.assertNotContains(response, "alex")
        self.assertNotContains(response, "maria")
