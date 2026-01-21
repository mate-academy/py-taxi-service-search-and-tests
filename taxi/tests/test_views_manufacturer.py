from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEquals(res, 200)


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        numbers_of_manufacturers = 6
        for manufacturer_id in range(numbers_of_manufacturers):
            Manufacturer.objects.create(
                name=f"test{manufacturer_id}",
                country=f"qwe{manufacturer_id}",
            )

    def test_manufacturer_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_view_url_accessible_by_name(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_uses_correct_template_name(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_manufacturer_pagination_is_five(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertTrue("is_paginated" in res.context)
        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(len(res.context["manufacturer_list"]), 5)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(pk__lte=5))
        )

    def test_lists_all_manufacturers(self):
        res = self.client.get(MANUFACTURER_URL + "?page=2")
        self.assertEqual(res.status_code, 200)
        self.assertTrue("is_paginated" in res.context)
        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(len(res.context["manufacturer_list"]), 1)


class ManufacturerCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer_create_url = reverse("taxi:manufacturer-create")

    def test_manufacturer_create_view_url_exists_at_desired_location(self):
        res = self.client.get("/manufacturers/create/")
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_create_view_url_accessible_by_name(self):
        res = self.client.get(self.manufacturer_create_url)
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_create_uses_correct_template_name(self):
        res = self.client.get(self.manufacturer_create_url)
        self.assertTemplateUsed(res, "taxi/manufacturer_form.html")

    def test_manufacturer_create(self):
        res = self.client.post(
            self.manufacturer_create_url,
            {"name": "BMW", "country": "Germany"}
        )
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/manufacturers/")
        self.assertEqual(Manufacturer.objects.get(pk=1).name, "BMW")


class ManufacturerUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.manufacturer_update_url = reverse(
            "taxi:manufacturer-update",
            args=[self.manufacturer.id]
        )

    def test_manufacturer_update_view_url_exists_at_desired_location(self):
        res = self.client.get(f"/manufacturers/{self.manufacturer.id}/update/")
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_update_view_url_accessible_by_name(self):
        res = self.client.get(self.manufacturer_update_url)
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_update_uses_correct_template_name(self):
        res = self.client.get(self.manufacturer_update_url)
        self.assertTemplateUsed(res, "taxi/manufacturer_form.html")

    def test_manufacturer_update(self):
        res = self.client.post(
            self.manufacturer_update_url,
            {"name": self.manufacturer.name, "country": "USA"}
        )
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/manufacturers/")
        self.assertEqual(self.manufacturer.country, "Germany")
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.country, "USA")


class ManufacturerDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.manufacturer_delete_url = reverse(
            "taxi:manufacturer-delete",
            args=[self.manufacturer.id]
        )

    def test_manufacturer_delete_view_url_exists_at_desired_location(self):
        res = self.client.get(f"/manufacturers/{self.manufacturer.id}/delete/")
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_delete_view_url_accessible_by_name(self):
        res = self.client.get(self.manufacturer_delete_url)
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_delete_uses_correct_template_name(self):
        res = self.client.get(self.manufacturer_delete_url)
        self.assertTemplateUsed(res, "taxi/manufacturer_confirm_delete.html")

    def test_manufacturer_delete(self):
        res = self.client.post(self.manufacturer_delete_url)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/manufacturers/")
        self.assertFalse(Manufacturer.objects.filter(id=self.manufacturer.id))
