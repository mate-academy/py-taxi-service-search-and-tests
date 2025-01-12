from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver
from django.contrib.auth import get_user_model


class DriverSearchTest(TestCase):
    def setUp(self):
        # Створення користувача
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(
            username="testuser",
            password="testpass")

        # Створення водіїв
        self.driver1 = Driver.objects.create(username="john_doe",
                                             license_number="12345")
        self.driver2 = Driver.objects.create(username="jane_smith",
                                             license_number="67890")

    def test_search_driver_by_username(self):
        response = self.client.get(reverse(
            "taxi:driver-list"), {"username": "john"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "jane_smith")
