from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer

MANUFACTURERS_FORMAT_URL = reverse("taxi:manufacturer-list")


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser", password="testpass123"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Tesla", country="USA")
        Manufacturer.objects.create(name="Ford", country="USA")

    def test_list_all_manufacturers_without_filter(self):
        response = self.client.get(MANUFACTURERS_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Tesla")
        self.assertContains(response, "Ford")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(MANUFACTURERS_FORMAT_URL, {"name": "Tes"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla")
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_search_no_results(self):
        response = self.client.get(MANUFACTURERS_FORMAT_URL, {"name": "BMW"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "There are no manufacturers in the service."
        )
        self.assertQuerysetEqual(response.context["manufacturer_list"], [])

    def test_search_form_retains_input(self):
        response = self.client.get(MANUFACTURERS_FORMAT_URL, {"name": "Tes"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="Tes"')
