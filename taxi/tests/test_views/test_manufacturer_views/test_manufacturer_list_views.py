from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer
from taxi.tests.test_views.initial_data import MANUFACTURER_LIST_URL


class ManufacturerListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_manufacturers = 8

        for manufacturer_id in range(1, number_of_manufacturers + 1):
            Manufacturer.objects.create(
                name=f"test_name_{manufacturer_id}",
                country=f"test_country_{manufacturer_id}",
            )

    def setUp(self):
        self.manufacturer = Manufacturer.objects.get(name="test_name_1")
        self.user = get_user_model().objects.create_user(
            username="test_username",
            license_number="ABC12346",
            password="Test1234q",
        )
        self.client.force_login(self.user)

    def test_manufacturers_pagination_is_five(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_lists_all_manufacturers(self):
        response = self.client.get(f"{MANUFACTURER_LIST_URL}?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_manufacturers_get_context_data(self):
        response = self.client.get(f"{MANUFACTURER_LIST_URL}?name=test")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("search_form" in response.context_data)
        self.assertEqual(
            response.context_data["search_form"].initial["name"],
            "test"
        )

    def test_manufacturers_get_queryset(self):
        response = self.client.get(f"{MANUFACTURER_LIST_URL}?name=test_name_1")
        queryset = response.context_data["object_list"]
        self.assertEqual(len(queryset), 1)
        self.assertEqual(queryset[0], self.manufacturer)

    def test_manufacturers_search_pagination(self):
        response = self.client.get(f"{MANUFACTURER_LIST_URL}?name=test&page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_manufacturers_search_no_page(self):
        response = self.client.get(f"{MANUFACTURER_LIST_URL}?name=nonexistent")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 0)
