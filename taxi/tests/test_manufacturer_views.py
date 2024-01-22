from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import ManufacturerNameSearchForm
from taxi.models import Manufacturer


class ManufacturerViewsTest(TestCase):
    MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
            password="testpassword",
        )

        self.client = Client()
        self.client.force_login(self.user)

        for _id in range(15):
            Manufacturer.objects.create(
                name=f"Test name {_id}"
            )

    def test_list_if_not_login(self):
        self.client.logout()
        res = self.client.get(self.MANUFACTURER_LIST_URL)
        self.assertRedirects(res, "/accounts/login/?next=/manufacturers/")

    def test_list_view_if_logged_in(self):
        res = self.client.get(self.MANUFACTURER_LIST_URL)

        self.assertEqual(str(res.context["user"]), str(self.user))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_list_view_pagination(self):
        res = self.client.get(self.MANUFACTURER_LIST_URL)

        self.assertTrue("is_paginated" in res.context)
        self.assertEqual(len(res.context["manufacturer_list"]), 5)

    def test_list_view_search(self):
        manufacturer = Manufacturer.objects.create(name="Audi")
        res = self.client.get("/manufacturers/?name=au")

        self.assertTrue("search_form" in res.context)
        self.assertIsInstance(
            res.context["search_form"],
            ManufacturerNameSearchForm
        )
        self.assertEqual(res.context["search_form"].initial["name"], "au")
        self.assertEqual(len(res.context["manufacturer_list"]), 1)
        self.assertEqual(res.context["manufacturer_list"][0], manufacturer)

    def test_list_view_invalid_search(self):
        res = self.client.get("/manufacturers/?name=")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["manufacturer_list"]), 5)
        self.assertFalse(res.context["search_form"].is_valid())
