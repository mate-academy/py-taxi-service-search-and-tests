from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test user",
            password="testPassword123",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test country",
        )
        self.car = Car.objects.create(
            manufacturer=self.manufacturer,
            model="Test model",
        )
        self.car.drivers.add(self.user)

    def test_search_driver(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "test user"}
        )
        self.assertContains(response, "test user")

    def test_search_manufacturer(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"manufacturer": "Test Manufacturer"}
        )
        self.assertContains(response, "Test Manufacturer")

    def test_search_car(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Test Model"})
        self.assertContains(response, "Test Model")
