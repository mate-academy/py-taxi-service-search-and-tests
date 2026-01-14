from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Driver, Car, Manufacturer

User = get_user_model()


class DriverSearchTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="12345",
            license_number="ADMIN001"
        )
        self.client.login(username="admin", password="12345")

        self.user1 = User.objects.create_user(
            username="john_doe",
            password="12345",
            license_number="JD12345"
        )
        self.user2 = User.objects.create_user(
            username="alice",
            password="12345",
            license_number="AL67890"
        )

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"}
        )

        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "alice")


class CarSearchTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345",
            license_number="TEST123"
        )
        self.client.login(username="testuser", password="12345")

        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

        self.car1 = Car.objects.create(
            model="Tesla Model S",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="BMW X5",
            manufacturer=self.manufacturer
        )

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Tesla"}
        )

        self.assertContains(response, "Tesla Model S")
        self.assertNotContains(response, "BMW X5")


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345",
            license_number="MAN123"
        )
        self.client.login(username="testuser", password="12345")

        self.m1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.m2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toy"}
        )

        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")
