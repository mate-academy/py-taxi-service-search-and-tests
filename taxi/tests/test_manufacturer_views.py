from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi import forms
from taxi.models import Car, Driver, Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="test_driver",
            license_number="test_license_number",
        )
        self.client.force_login(self.user)

        number_of_manufacturer = 12

        for manufacturer_id in range(number_of_manufacturer):
            Manufacturer.objects.create(
                name=f"manufacturer {manufacturer_id}",
                country=f"test_country {manufacturer_id}",
            )

    def test_view_url_exists(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_view_have_search_form_context(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], forms.ManufacturerSearchForm
        )

    def test_existing_pagination(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_pagination_paged(self):
        response = self.client.get(MANUFACTURER_URL + "?page=3")
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

    def test_correct_query_set(self):
        response = self.client.get(
            MANUFACTURER_URL, {"name": "manufacturer 3"}
        )
        self.assertContains(response, "manufacturer 3")
        self.assertNotContains(response, "manufacturer 4")

    def test_update_manufacturer_view_exist(self):
        response = self.client.get(
            reverse(
                "taxi:manufacturer-update",
                args=[Manufacturer.objects.first().pk]
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_manufacturer_view_exist(self):
        response = self.client.get(
            reverse(
                "taxi:manufacturer-delete",
                args=[Manufacturer.objects.first().pk]
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_create_manufacturer_view_exist(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 200)
