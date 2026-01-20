from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class PublicManufacturerTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test Country",
        )

    def test_manufacturer_list_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_create_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_update_login_required(self):
        response = self.client.get(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.id])
        )
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_delete_login_required(self):
        response = self.client.get(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        )
        self.assertNotEqual(response.status_code, 200)


class BasePrivateManufacturerTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test manufacturer",
            country="Test Country",
        )
        self.driver = get_user_model().objects.create_user(
            username="Test", password="Testpass123"
        )
        self.client.force_login(self.driver)


class PrivateManufacturerListTests(BasePrivateManufacturerTests):
    MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
    VIEW_PAGINATED_BY = 5

    def setUp(self):
        super().setUp()
        for i in range(1, 11):
            Manufacturer.objects.create(
                name=f"Test {i}",
                country=f"Test Country {i}",
            )

    def test_manufacturer_list_template(self):
        response = self.client.get(self.MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_pagination(self):
        response = self.client.get(self.MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(
            len(response.context["manufacturer_list"]), self.VIEW_PAGINATED_BY
        )

    def test_manufacturer_list_search(self):
        response = self.client.get(self.MANUFACTURER_LIST_URL + "?name=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)
        self.assertContains(response, "Test 1")
        self.assertNotContains(response, "Test 2")

    def test_manufacturer_search_pagination(self):
        response = self.client.get(
            self.MANUFACTURER_LIST_URL + "?name=Test&page=2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(
            len(response.context["manufacturer_list"]), self.VIEW_PAGINATED_BY
        )


class PrivateManufacturerCreateTests(BasePrivateManufacturerTests):
    def test_manufacturer_create_uses_correct_template(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_manufacturer_create_post(self):
        form_data = {
            "name": "Test new manufacturer",
            "country": "Test Country",
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])
        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])


class PrivateManufacturerUpdateTests(BasePrivateManufacturerTests):
    def test_manufacturer_update_uses_correct_template(self):
        response = self.client.get(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_manufacturer_update_post(self):
        form_data = {
            "name": "Updated manufacturer",
            "country": "Updated Country",
        }
        self.client.post(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.id]),
            data=form_data,
        )
        updated_manufacturer = Manufacturer.objects.get(
            id=self.manufacturer.id
        )
        self.assertEqual(updated_manufacturer.name, form_data["name"])
        self.assertEqual(updated_manufacturer.country, form_data["country"])


class PrivateManufacturerDeleteTests(BasePrivateManufacturerTests):
    def test_manufacturer_delete_uses_correct_template(self):
        response = self.client.get(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_confirm_delete.html"
        )

    def test_manufacturer_delete_post(self):
        self.client.post(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        )
        manufacturers = Manufacturer.objects.filter(id=self.manufacturer.id)
        self.assertEqual(len(manufacturers), 0)
