from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

DRIVER_LIST_URL = reverse("taxi:driver-list")


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="password123",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

        self.driver1 = get_user_model().objects.create_user(
            username="john_doe",
            password="password123",
            license_number="ABD12345",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="alice_smith",
            password="password123",
            license_number="AAD12345",
        )

    def test_search_by_driver_username(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "john"})
        driver_list = response.context["driver_list"]

        self.assertIn(self.driver1, driver_list)
        self.assertNotIn(self.driver2, driver_list)

    def test_search_driver_username_is_case_insensitive(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "JOHN"})
        driver_list = response.context["driver_list"]

        self.assertIn(self.driver1, driver_list)

    def test_empty_driver_search_returns_all(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": ""})
        driver_list = response.context["driver_list"]

        self.assertEqual(len(driver_list), 3)
