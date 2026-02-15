from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Driver

User = get_user_model()


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")

        Driver.objects.create(
            username="john", first_name="John",
            last_name="Doe", license_number="ABC123"
        )
        Driver.objects.create(
            username="jane", first_name="Jane",
            last_name="Smith", license_number="XYZ789"
        )

    def test_search_by_username_returns_correct_results(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"search": "jan"})
        self.assertContains(response, "jane")
        self.assertNotContains(response, "john")

    def test_search_empty_returns_all_results(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertContains(response, "john")
        self.assertContains(response, "jane")

    def test_search_no_match_returns_empty(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"search": "alex"})
        self.assertContains(
            response, "There are no drivers in the service."
        )
