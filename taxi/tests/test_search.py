from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver
from django.contrib.auth import get_user_model


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.force_login(self.user)

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
            model="Mustang",
            manufacturer=self.manufacturer2
        )

        self.driver1 = Driver.objects.create_user(
            username="driver1", password="pass123", license_number="QWE12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2", password="pass123", license_number="ZXC12345"
        )

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "toy"}
        )
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_manufacturer_search_empty_query_returns_all(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Ford")

    def test_car_search_by_model(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "mus"})
        self.assertContains(response, "Mustang")
        self.assertNotContains(response, "Corolla")

    def test_car_search_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "COROLLA"}
        )
        self.assertContains(response, "Corolla")

    def test_driver_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "1"}
        )
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")

    def test_driver_search_partial_match(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "driver"}
        )
        self.assertContains(response, "driver1")
        self.assertContains(response, "driver2")

    def test_manufacturer_search_returns_correct_result(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "toy"}
        )
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")
