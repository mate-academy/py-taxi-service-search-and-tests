from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from taxi.models import Manufacturer


class ManufacturerViewTest(TestCase):
    def setUp(self):
        self.username = "usertest"
        self.password = "testpassword456"
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="United Kingdom",
        )
        self.client.force_login(self.user)

    def test_login_required_views(self):
        login_required_urls = [
            reverse_lazy("taxi:manufacturer-list"),
            reverse_lazy("taxi:manufacturer-create"),
            reverse_lazy("taxi:manufacturer-update", args=[1]),
            reverse_lazy("taxi:manufacturer-delete", args=[1]),
        ]

        for url in login_required_urls:
            self.client.logout()
            response = self.client.get(url)
            expected_url = f"/accounts/login/?next={url}"

            self.assertNotEqual(response.status_code, 200)
            self.assertRedirects(response, expected_url)

            self.client.force_login(self.user)
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)

    def create_manufacturers(self, instance_count):
        for manufacturer_id in range(instance_count):
            Manufacturer.objects.create(
                name=f"name {manufacturer_id}",
                country=f"country {manufacturer_id}",
            )

    def test_manufacturer_list_view_pagination(self):
        self.create_manufacturers(10)
        response = self.client.get(reverse_lazy("taxi:manufacturer-list"))

        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(len(response.context["manufacturer_list"]) == 5)

    def test_manufacturer_list_view_search(self):
        self.create_manufacturers(10)
        response = self.client.get(
            reverse_lazy("taxi:manufacturer-list"),
            {"search": "Test Manufacturer"}
        )

        self.assertContains(response, self.manufacturer.name)
        self.assertTrue(len(response.context["manufacturer_list"]) == 1)

        response = self.client.get(
            reverse_lazy("taxi:manufacturer-list"), {"search": "name"}
        )

        self.assertTrue(len(response.context["manufacturer_list"]) == 5)

    def test_manufacturer_list_view_not_result_search(self):
        self.create_manufacturers(10)
        response = self.client.get(
            reverse_lazy("taxi:manufacturer-list"), {"search": "qwerty"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["manufacturer_list"])

    def test_manufacturer_list_view_empty_search(self):
        self.create_manufacturers(10)
        response = self.client.get(
            reverse_lazy("taxi:manufacturer-list"), {"search": ""}
        )

        self.assertTrue(len(response.context["manufacturer_list"]) == 5)

    def test_manufacturer_list_view_search_form_saves_get_parameters(self):
        response = self.client.get(
            reverse_lazy("taxi:manufacturer-list"),
            {"search": "Test Manufacturer", "color": "blue"},
        )
        self.assertContains(
            response, '<input type="hidden" name="color" value="blue">'
        )
        self.assertNotContains(response, '<input type="hidden" name="search"')

    def test_manufacturer_delete_view(self):
        response = self.client.get(reverse_lazy("taxi:manufacturer-list"))
        self.assertContains(response, self.manufacturer.name)

        response = self.client.post(
            reverse_lazy(
                "taxi:manufacturer-delete", args=[self.manufacturer.id]
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=self.manufacturer.id).exists()
        )

    def test_create_manufacturer_view(self):
        form_data = {
            "name": "name1",
            "country": "country1",
        }

        self.assertFalse(
            Manufacturer.objects.filter(name=form_data["name"]).exists()
        )

        response = self.client.post(
            reverse_lazy("taxi:manufacturer-create"), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("taxi:manufacturer-list"))
        self.assertTrue(
            Manufacturer.objects.filter(name=form_data["name"]).exists()
        )

    def test_update_manufacturer_view(self):
        form_data = {
            "name": "name1",
            "country": self.manufacturer.country,
        }

        self.assertFalse(
            Manufacturer.objects.filter(name=form_data["name"]).exists()
        )

        response = self.client.post(
            reverse_lazy(
                "taxi:manufacturer-update", args=[self.manufacturer.pk]
            ),
            data=form_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Manufacturer.objects.filter(name=form_data["name"]).exists()
        )
