from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/")


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

        number_of_manufacturers = 10
        for manufacturer_id in range(1, number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"Name{manufacturer_id}",
                country=f"Country{manufacturer_id}",
            )

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()[:5]
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_view_uses_correct_template(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_logged_in_access(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_five(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_query_search_filter(self):
        response = self.client.get(f"{MANUFACTURERS_URL}?name=Name1")
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains="Name1")
        )
