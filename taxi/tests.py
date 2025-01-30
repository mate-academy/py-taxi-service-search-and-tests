from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer
from django.contrib.auth import get_user_model


class TaxiSearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.driver = get_user_model().objects.create_user(
            username="test driver",
            password="test pass123",
            license_number="ABC12345"
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer
        )

    def test_manufacturer_search(self):
        self.client.login(username="test driver", password="test pass123")
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Manufacturer")

    def test_car_search(self):
        self.client.login(username="test driver", password="test pass123")
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Car")

    def test_driver_search(self):
        self.client.login(username="test driver", password="test pass123")
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test driver")


class ManufacturerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.driver = Driver.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)

    def test_manufacturer_create(self):
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            {"name": "New Manufacturer", "country": "New Country"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Manufacturer.objects.filter(name="New Manufacturer").exists()
        )

    def test_manufacturer_update(self):
        response = self.client.post(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.id]),
            {"name": "Updated Name", "country": "Updated Country"}
        )
        self.assertEqual(response.status_code, 302)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "Updated Name")

    def test_manufacturer_delete(self):
        response = self.client.post(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=self.manufacturer.id).exists()
        )
