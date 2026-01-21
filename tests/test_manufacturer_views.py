from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class TestManufacturerViewsLoginRequired(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry",
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


class BaseManufacturerTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry",
        )
        self.driver = get_user_model().objects.create_user(
            username="TestDriver3", password="TestPassword3"
        )
        self.client.force_login(self.driver)


class TestManufacturerList(BaseManufacturerTest):
    manufacturer_list_url = reverse("taxi:manufacturer-list")
    paginated_by = 5

    def setUp(self):
        super().setUp()
        for i in range(1, 16):
            Manufacturer.objects.create(
                name=f"TestManufacturer{i}",
                country=f"TestCountry{i}",
            )

    def test_manufacturer_list_template(self):
        response = self.client.get(self.manufacturer_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_pagination(self):
        response = self.client.get(self.manufacturer_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(
            len(response.context["manufacturer_list"]), self.paginated_by
        )

    def test_manufacturer_list_search(self):
        response = self.client.get(self.manufacturer_list_url + "?name=4")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)
        self.assertContains(response, "TestManufacturer4")
        self.assertNotContains(response, "TestManufacturer5")


class TestManufacturerCreate(BaseManufacturerTest):
    def test_manufacturer_create_template(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_manufacturer_create(self):
        form_data = {
            "name": "NewTestManufacturer",
            "country": "TestCountry",
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])
        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])


class TestManufacturerUpdate(BaseManufacturerTest):
    def test_manufacturer_update_template(self):
        response = self.client.get(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_manufacturer_update(self):
        data = {
            "name": "UpdatedTestManufacturer",
            "country": "UpdatedCountry",
        }
        self.client.post(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.id]),
            data=data,
        )
        updated_manufacturer = Manufacturer.objects.get(
            id=self.manufacturer.id
        )
        self.assertEqual(updated_manufacturer.name, data["name"])
        self.assertEqual(updated_manufacturer.country, data["country"])


class TestManufacturerDelete(BaseManufacturerTest):
    def test_manufacturer_delete_template(self):
        response = self.client.get(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_confirm_delete.html"
        )

    def test_manufacturer_delete(self):
        self.client.post(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        )
        manufacturers = Manufacturer.objects.filter(id=self.manufacturer.id)
        self.assertEqual(len(manufacturers), 0)
