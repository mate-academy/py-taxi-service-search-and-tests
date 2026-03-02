from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer

User = get_user_model()


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test12345"
        )

        # 🔐 логінимо одразу
        self.client.login(
            username="testuser",
            password="test12345"
        )

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Ford", country="USA")

    def test_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toy"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

    def test_search_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"}
        )

        self.assertContains(response, "Toyota")

    def test_search_empty_query_returns_all(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list")
        )

        self.assertEqual(
            len(response.context["manufacturer_list"]),
            3
        )