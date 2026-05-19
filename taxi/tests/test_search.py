from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")

    def test_search_by_name_returns_match(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Toyota"}
        )
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

    def test_search_empty_returns_all(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": ""}
        )
        self.assertContains(response, "Toyota")
        self.assertContains(response, "BMW")


class CarSearchTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="loginuser",
            password="test1234",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        Car.objects.create(model="Camry", manufacturer=manufacturer)
        Car.objects.create(model="Corolla", manufacturer=manufacturer)

    def test_search_by_model_returns_match(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Camry"}
        )
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Corolla")

    def test_search_empty_returns_all(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": ""})
        self.assertContains(response, "Camry")
        self.assertContains(response, "Corolla")


class DriverSearchTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)
        get_user_model().objects.create_user(
            username="alice",
            password="test1234",
            license_number="DEF67890",
        )

    def test_search_by_username_returns_match(self) -> None:
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "alice"}
        )
        drivers = response.context["driver_list"]
        self.assertTrue(any(d.username == "alice" for d in drivers))
        self.assertFalse(any(d.username == "testuser" for d in drivers))

    def test_search_empty_returns_all(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": ""}
        )
        self.assertContains(response, "alice")
        self.assertContains(response, "testuser")
