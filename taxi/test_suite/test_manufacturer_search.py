from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer

User = get_user_model()


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Tesla", country="USA")

    def test_search_by_name_returns_correct_results(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"search": "Tes"})
        self.assertContains(response, "Tesla")
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_search_empty_returns_all_results(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Ford")
        self.assertContains(response, "Tesla")

    def test_search_no_match_returns_empty(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"search": "BMW"})
        self.assertContains(
            response, "There are no manufacturers in the service."
        )
