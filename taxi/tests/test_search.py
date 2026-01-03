from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Driver, Car


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="Password123",
            license_number="USR12345"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

    def test_car_search_by_model(self):
        Car.objects.create(model="BMW X5", manufacturer=self.manufacturer)
        Car.objects.create(model="Audi A4", manufacturer=self.manufacturer)

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "BMW"}
        )

        self.assertContains(response, "BMW X5")
        self.assertNotContains(response, "Audi A4")

    def test_driver_search_by_username(self):
        Driver.objects.create_user(
            username="john_doe",
            password="12345",
            license_number="ABC12345"
        )
        Driver.objects.create_user(
            username="anna",
            password="12345",
            license_number="DEF67890"
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"}
        )

        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "anna")

    def test_manufacturer_search_by_name(self):
        Manufacturer.objects.create(name="BMW_test", country="DE")
        Manufacturer.objects.create(name="Audi_test", country="DE")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "BMW_test"}
        )

        self.assertContains(response, "BMW_test")
        self.assertNotContains(response, "Audi_test")
