from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

LOGIN_PAGE = reverse("login") + "?next=/manufacturers/"
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerListTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, LOGIN_PAGE)


class PrivateManufacturerListTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_user(
            "test1",
            "password1",
        )
        for i in range(15):
            Manufacturer.objects.create(
                name=f"Manufacturer{i}", country=f"Country{i}"
            )

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.response = self.client.get(MANUFACTURER_URL)

    def test_retrieve_manufacturers(self):
        manufacturer_list = Manufacturer.objects.all()
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(
            list(self.response.context["manufacturer_list"]),
            list(manufacturer_list)[:5],
        )
        self.assertTemplateUsed(self.response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_search(self):
        response = self.client.get(MANUFACTURER_URL + "?name=Man")
        queryset_searched = Manufacturer.objects.filter(
            name__icontains="Man",
        )
        self.assertQuerysetEqual(
            response.context["manufacturer_list"], queryset_searched[:5]
        )

    def test_manufacturer_list_pagination_is_five(self):
        self.assertTrue("is_paginated" in self.response.context)
        self.assertEqual(len(self.response.context["manufacturer_list"]), 5)
