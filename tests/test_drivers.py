from django.urls import reverse
from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class DriverSearchTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.login(username="testuser", password="password123")

        Driver.objects.create(
            username="driver_john_doe",
            password="testpassword",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        Driver.objects.create(
            username="driver_jane_smith",
            password="testpassword1",
            first_name="Jane",
            last_name="Smith",
            license_number="XYZ67890"
        )
        Driver.objects.create(
            username="driver_alice_johnson",
            password="testpassword2",
            first_name="Alice",
            last_name="Johnson",
            license_number="LMN54321"
        )

    def test_search_by_name(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=john"
        )
        self.assertContains(response, "driver_john")
        self.assertNotContains(response, "driver_jane")

    def test_search_by_last_name(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=smith"
        )
        self.assertContains(response, "driver_jane")
        self.assertNotContains(response, "driver_john")

    def test_search_empty(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=NonExistentDriver"
        )
        self.assertContains(
            response, "There are no drivers in the service."
        )
