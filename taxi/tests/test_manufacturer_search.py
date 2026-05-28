from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer


class ManufacturerSearchTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="test12345"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        self.manufacturer2 = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

        self.manufacturer3 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

    def test_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toy"}
        )

        self.assertEqual(response.status_code, 200)

        manufacturers = response.context["manufacturer_list"]

        self.assertEqual(len(manufacturers), 1)
        self.assertEqual(manufacturers[0].name, "Toyota")

    def test_search_empty_query_returns_all(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        manufacturers = response.context["manufacturer_list"]

        self.assertEqual(len(manufacturers), 3)

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Unknown"}
        )

        manufacturers = response.context["manufacturer_list"]

        self.assertEqual(len(manufacturers), 0)

    def test_search_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "tesla"}
        )

        manufacturers = response.context["manufacturer_list"]

        self.assertEqual(len(manufacturers), 1)
        self.assertEqual(manufacturers[0].name, "Tesla")

    def test_search_partial_match(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Te"}
        )

        manufacturers = response.context["manufacturer_list"]

        self.assertTrue(
            all("te" in m.name.lower() for m in manufacturers)
        )

    def test_manufacturer_list_view_status_code(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()

        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 302)
