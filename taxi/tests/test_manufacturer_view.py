from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password",
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_get_context_data(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "test"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], ManufacturerSearchForm
        )
        self.assertEqual(
            response.context_data["search_form"].initial["name"], "test"
        )

    def test_get_query_with_no_filters(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer1.name)
        self.assertContains(response, self.manufacturer2.name)

    def test_get_query_with_filters(self):
        response = self.client.get(
            MANUFACTURER_URL, {"name": self.manufacturer1.name}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
