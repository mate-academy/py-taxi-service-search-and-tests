from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURERS_LIST_URL = reverse("taxi:manufacturer-list")


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.login(username="testuser", password="password")

        self.manufacturer1 = Manufacturer.objects.create(name="Toyota")
        self.manufacturer2 = Manufacturer.objects.create(name="Ford")
        self.manufacturer3 = Manufacturer.objects.create(name="General Motors")

    def test_search_no_query(self):
        response = self.client.get(MANUFACTURERS_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Ford")
        self.assertContains(response, "General Motors")

    def test_search_with_query(self):
        response = self.client.get(MANUFACTURERS_LIST_URL, {"name": "toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")
        self.assertNotContains(response, "General Motors")

    def test_search_with_partial_match_query(self):
        response = self.client.get(MANUFACTURERS_LIST_URL, {"name": "ord"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ford")
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "General Motors")

    def test_search_with_no_results(self):
        response = self.client.get(MANUFACTURERS_LIST_URL,
                                   {"name": "nonexistent"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Ford")
        self.assertNotContains(response, "General Motors")
