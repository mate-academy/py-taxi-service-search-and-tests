from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer
from taxi.tests import fixtures

LIST_URL = reverse("taxi:manufacturer-list")
CREATE_URL = reverse("taxi:manufacturer-create")
UPDATE_URL = reverse("taxi:manufacturer-update", kwargs={"pk": 1})
DELETE_URL = reverse("taxi:manufacturer-delete", kwargs={"pk": 1})


class PublicManufacturerViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        fixtures.fill_db()

    def test_list_view_login_required_and_redirect(self):
        response = self.client.get(LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'{reverse("login")}?next={LIST_URL}')

    def test_create_view_login_required_and_redirect(self):
        response = self.client.get(CREATE_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'{reverse("login")}?next={CREATE_URL}')

    def test_update_view_login_required_and_redirect(self):
        response = self.client.get(UPDATE_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'{reverse("login")}?next={UPDATE_URL}')

    def test_delete_view_login_required_and_redirect(self):
        response = self.client.get(DELETE_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'{reverse("login")}?next={DELETE_URL}')


class PrivateManufacturerViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        fixtures.fill_db()

    def setUp(self):
        self.client.force_login(get_user_model().objects.get(pk=1))

    def test_list_view_should_use_defined_template(self):
        response = self.client.get(LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_list_view_context_contains_custom_object_name_key(self):
        response = self.client.get(LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertIn("manufacturer_list", response.context)

    def test_list_view_is_paginated_by_5(self):
        response = self.client.get(LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context.get("is_paginated"))
        self.assertEqual(len(response.context.get("manufacturer_list")), 5)

    def test_list_view_correct_num_of_entries_on_next_page(self):
        response = self.client.get(LIST_URL + "?page=2")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context.get("is_paginated"))
        self.assertEqual(len(response.context.get("manufacturer_list")), 3)

    def test_list_view_context_contain_search_by_name_and_it_works(self):
        response = self.client.get(LIST_URL + "?name=i")
        manufacturers_ = list(
            response.context.get("manufacturer_list").values("name", "country")
        )

        self.assertIn("search_form", response.context)
        self.assertTrue(len(manufacturers_) == 2)
        self.assertCountEqual(fixtures.custom_manufacturers, manufacturers_)

    def test_create_view(self):
        data = {"name": "custom_name", "country": "custom_country"}

        response = self.client.post(CREATE_URL, data)

        self.assertRedirects(response, LIST_URL)
        self.assertTrue(
            Manufacturer.objects.filter(name="custom_name").exists()
        )

    def test_update_view(self):
        data = {"name": "custom_name", "country": "custom_country"}
        before = Manufacturer.objects.get(pk=1)

        response = self.client.post(UPDATE_URL, data)
        after = Manufacturer.objects.get(pk=1)

        self.assertRedirects(response, LIST_URL)
        self.assertEqual(after.name, "custom_name")
        self.assertEqual(after.country, "custom_country")
        self.assertEqual(after.id, before.id)

    def test_delete_view(self):
        response = self.client.post(DELETE_URL)

        self.assertRedirects(response, LIST_URL)
        self.assertFalse(Manufacturer.objects.filter(pk=1).exists())
