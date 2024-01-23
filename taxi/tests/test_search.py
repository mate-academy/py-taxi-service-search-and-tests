from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class SearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="test_user",
            password="test_pass"
        )
        self.client.force_login(self.user)
        get_user_model().objects.create_user(
            username="alex2",
            password="test123",
            license_number="ABV12345"
        )
        Manufacturer.objects.create(
            name="Test Manufacturer",
            country="United States"
        )
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="United States"
        )
        Car.objects.create(model="test", manufacturer=manufacturer)
        Car.objects.create(model="RX", manufacturer=manufacturer)

    def test_search_manufacturer(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Manufacturer", response.content.decode())

    def test_search_car(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "RX"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("RX", response.content.decode())

    def test_search_driver(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "alex"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("alex2", response.content.decode())
