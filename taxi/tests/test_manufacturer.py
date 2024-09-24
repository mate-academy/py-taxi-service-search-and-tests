from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class ManufacturerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(10):
            (Manufacturer.objects.
             create(name=f"Mercedes_{i}", country="Germany"))

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="Admin", password="hard", email="anton@gmail.com"
        )
        self.client.force_login(self.admin_user)

    def test_connection(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_pagination_first_page(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_pagination_second_page(self):
        response = (self.client.
                    get(reverse("taxi:manufacturer-list"), {"page": 2}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_search_form_with_one_result(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Mercedes_0"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("manufacturer_list", response.context)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        (self.assertEqual
         (response.context["manufacturer_list"][0].name, "Mercedes_0"))

    def tes_search_form_with_zero_result(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Pampam"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response.context, "manufacturer_list")
        self.assertEqual(len(response.context["manufacturer_list"]), 0)

    def test_search_form_all_results(self):
        response = (self.client.
                    get(reverse("taxi:manufacturer-list"), {"name": ""}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("manufacturer_list", response.context)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_search_form_all_results_second_page(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "", "page": 2}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("manufacturer_list", response.context)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)
        (self.assertTrue
         ("Mercedes_5" == response.context["manufacturer_list"][0].name))
