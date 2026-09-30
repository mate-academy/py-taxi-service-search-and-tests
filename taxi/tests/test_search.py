from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class SearchTest(TestCase):

    def setUp(self):
        self.user = Driver.objects.create_user(
            username="admin",
            password="password123",
            license_number="ADMIN123"
        )

        self.client.login(
            username="admin",
            password="password123"
        )

    def test_search_driver_by_username(self):
        Driver.objects.create_user(
            username="admin123",
            password="password123",
            license_number="ABC123"
        )

        Driver.objects.create_user(
            username="marek123",
            password="password123",
            license_number="LIC456"
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "admin"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin123")
        self.assertNotContains(response, "marek123")

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Rover",
            country="UK"
        )

        Car.objects.create(
            model="Streetwise",
            manufacturer=manufacturer
        )

        Car.objects.create(
            model="LandRover",
            manufacturer=manufacturer
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Streetwise"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Streetwise")
        self.assertNotContains(response, "LandRover")

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(
            name="Rover",
            country="UK"
        )

        Manufacturer.objects.create(
            name="Mercedes",
            country="Germany"
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Rover"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rover")
        self.assertNotContains(response, "Mercedes")

    def test_search_no_results(self):
        Manufacturer.objects.create(
            name="Rover",
            country="UK"
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Mercedes"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["manufacturer_list"]),
            0
        )
