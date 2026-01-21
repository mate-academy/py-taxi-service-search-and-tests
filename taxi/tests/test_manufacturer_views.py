from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:manufacturer-list")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=" + self.url)

    def test_context_contains_search_form(self):
        response = self.client.get(self.url + "?name=test")
        self.assertIn("search_form", response.context)
        form = response.context["search_form"]
        self.assertEqual(form.initial.get("name"), "test")

    def test_search_partial_match(self):
        Manufacturer.objects.create(name="test1", country="test_country")
        Manufacturer.objects.create(name="test2", country="test_country")
        response = self.client.get(self.url + "?name=test1")

        manufacturer_names = [
            manufacturer.name
            for manufacturer in response.context["manufacturer_list"]
        ]
        self.assertIn("test1", manufacturer_names)
        self.assertNotIn("test2", manufacturer_names)

    def test_search_empty(self):
        Manufacturer.objects.create(name="test1", country="test_country")
        Manufacturer.objects.create(name="test2", country="test_country")

        response = self.client.get(self.url)
        manufacturer_names = [
            manufacturer.name
            for manufacturer in response.context["manufacturer_list"]
        ]
        self.assertIn("test1", manufacturer_names)
        self.assertIn("test2", manufacturer_names)

    def test_pagination(self):
        Manufacturer.objects.bulk_create([
            Manufacturer(name=f"test{i}", country="test_country")
            for i in range(10)
        ])

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_pagination_with_search(self):
        Manufacturer.objects.create(name="audi", country="test_country")
        Manufacturer.objects.bulk_create([
            Manufacturer(name=f"test{i}", country="test_country")
            for i in range(9)
        ])
        response = self.client.get(self.url + "?name=test&page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 4)


class ManufacturerCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )

        self.client.force_login(self.user)
        self.url = reverse("taxi:manufacturer-create")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=" + self.url)

    def test_status_code_200_and_uses_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")
        self.assertEqual(response.status_code, 200)

    def test_create_manufacturer(self):
        data = {
            "name": "test",
            "country": "test_country",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Manufacturer.objects.count(), 1)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

    def test_create_manufacturer_invalid(self):
        data = {
            "name": "",
            "country": "test_country",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Manufacturer.objects.count(), 0)
        self.assertFormError(
            response.context["form"], "name", "This field is required."
        )


class ManufacturerUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test", country="test_country"
        )
        self.url = reverse(
            "taxi:manufacturer-update", kwargs={"pk": self.manufacturer.pk}
        )

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=" + self.url)

    def test_status_code_200_and_uses_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")
        self.assertEqual(response.status_code, 200)

    def test_update_manufacturer(self):
        data = {
            "name": "new_test",
            "country": "test_country",
        }
        old_manufacturer_name = self.manufacturer.name
        response = self.client.post(self.url, data)
        self.manufacturer.refresh_from_db()
        self.assertNotEqual(self.manufacturer.name, old_manufacturer_name)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

    def test_update_manufacturer_invalid(self):
        data = {
            "name": "",
            "country": "test_country",
        }
        old_manufacturer_name = self.manufacturer.name
        response = self.client.post(self.url, data)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, old_manufacturer_name)
        self.assertFormError(
            response.context["form"], "name", "This field is required."
        )


class ManufacturerDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test", country="test_country"
        )
        self.url = reverse(
            "taxi:manufacturer-delete", kwargs={"pk": self.manufacturer.pk}
        )

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=" + self.url)

    def test_status_code_200_and_uses_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_confirm_delete.html"
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_manufacturer(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertEqual(Manufacturer.objects.count(), 0)
