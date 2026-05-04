from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class ManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            email="",
            password="password",
            license_number="GF43212",
        )

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        self.manufacturer2 = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

    def test_search_manufacturer(self):
        self.client.force_login(self.user)

        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Toy"})

        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Tesla")
        self.assertContains(response, "")

        self.assertEqual(response.status_code, 200)

    def test_search_manufacturer_all(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": ""}
        )
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Tesla")

    def test_search_no_results_manufacturer(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "NonExistent"}
        )

        self.assertEqual(len(response.context["manufacturer_list"]), 0)
