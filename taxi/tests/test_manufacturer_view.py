from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
PAGINATION = 2


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test.user",
            "user12345",
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_response_with_correct_template(self):
        response = self.client.get(MANUFACTURERS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_paginated_correctly(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Chevrolet", country="USA")
        response = self.client.get(MANUFACTURERS_URL)

        self.assertEqual(
            len(response.context["manufacturer_list"]), PAGINATION
        )

    def test_manufacturer_list_ordered_by_name(self):
        response = self.client.get(MANUFACTURERS_URL)
        man_list = Manufacturer.objects.all().order_by("name")
        manufacturer_context = response.context["manufacturer_list"]

        self.assertEqual(
            list(manufacturer_context),
            list(man_list[: len(manufacturer_context)]),
        )

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Chevrolet", country="USA")
        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer_form(self):
        response = self.client.get(MANUFACTURERS_URL + "?name=Lincoln")

        self.assertContains(response, "Lincoln")
        self.assertNotContains(response, "Mazda")
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
