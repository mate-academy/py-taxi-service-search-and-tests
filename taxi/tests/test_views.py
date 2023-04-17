from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerListViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertRedirects(response, '/accounts/login/?next=/manufacturers/')


class PrivateManufacturerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 manufacturers for pagination tests
        number_of_manufacturers = 13

        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"TestName {manufacturer_id}",
                country=f"TestCountry {manufacturer_id}",
            )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "test1234"
        )

        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_pagination_is_5(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_lists_all_manufacturers(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(MANUFACTURERS_URL+"?page=3")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_search_form(self):
        response = self.client.get(MANUFACTURERS_URL+"?name=1")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 4)
