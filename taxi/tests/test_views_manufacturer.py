from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_manufacturers_list_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/")


class PrivateManufacturerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for manufacturer_id in range(8):
            Manufacturer.objects.create(name=f"Test {manufacturer_id}")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test password"
        )
        self.client.force_login(self.user)

    def test_manufacturer_pagination_is_five(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_pagination_second_page(self):
        response = self.client.get(MANUFACTURER_LIST_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 3)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {
            "name": "Test name",
            "country": "Test country"
        }
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            data=form_data
        )
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])
        self.assertRedirects(response, "/manufacturers/")

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.get(pk=1)
        response = self.client.post(
            reverse("taxi:manufacturer-delete", kwargs={"pk": manufacturer.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(pk=manufacturer.id).exists()
        )

    def test_manufacturer_search_matches_found(self):
        response = self.client.get("/manufacturers/?name=Test+1")
        searching_manufacturer = Manufacturer.objects.filter(name="Test 1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(searching_manufacturer)
        )

    def test_manufacturer_search_no_matches_found(self):
        response = self.client.get("/manufacturers/?name=Fake+name")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "There are no manufacturers in the service."
        )

    def test_pagination_manufacturer_search_with_value_current_page(self):
        response = self.client.get("/manufacturers/?name=Test")
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_pagination_manufacturer_search_with_value_next_page(self):
        response = self.client.get("/manufacturers/?name=Test&page=2")
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 3)
