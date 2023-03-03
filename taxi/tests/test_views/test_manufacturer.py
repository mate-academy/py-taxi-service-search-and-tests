from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test manufacturer",
            country="test country"
        )

    def test_manufacturer_list_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_create_login_required(self):
        res = self.client.get(reverse("taxi:manufacturer-create"))

        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_update_login_required(self):
        res = self.client.get(reverse(
            "taxi:manufacturer-update", kwargs={"pk": self.manufacturer.id}
        ))

        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_delete_login_required(self):
        res = self.client.get(reverse(
            "taxi:manufacturer-delete", kwargs={"pk": self.manufacturer.id}
        ))

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="first_manufacturer",
            country="test_country"
        )
        number_of_manufacturers = 7

        for manufacturer in range(2, number_of_manufacturers):
            Manufacturer.objects.create(
                id=manufacturer,
                name=f"{manufacturer}name",
                country="test country",
            )

        self.queryset = Manufacturer.objects.all()

        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)

        self.assertEqual(response.status_code, 200)

    def test_manufacturer_create_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))

        self.assertEqual(response.status_code, 200)

    def test_manufacturer_update_login_required(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-update", kwargs={"pk": self.manufacturer.id}
        ))

        self.assertEqual(response.status_code, 200)

    def test_manufacturer_delete_login_required(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-delete", kwargs={"pk": self.manufacturer.id}
        ))

        self.assertEqual(response.status_code, 200)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURERS_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(self.queryset),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_pagination_is_five(self):
        response = self.client.get(MANUFACTURERS_URL)

        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)
