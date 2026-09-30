from django.urls import reverse

from taxi.forms import SearchForm
from taxi.models import Manufacturer
from taxi.tests.base import LoggedInTestCase

MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PrivateManufacturerCreateTest(LoggedInTestCase):
    def test_renders_form(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_create_manufacturer_success(self):
        data = {"name": "Toyota", "country": "Japan"}
        response = self.client.post(MANUFACTURER_CREATE_URL, data=data)

        self.assertRedirects(response, MANUFACTURER_LIST_URL)
        self.assertTrue(
            Manufacturer.objects.filter(
                name="Toyota", country="Japan"
            ).exists()
        )

    def test_create_manufacturer_fail_invalid_data(self):
        invalid_data = {"name": ""}
        response = self.client.post(MANUFACTURER_CREATE_URL, invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Manufacturer.objects.exists())


class PrivateManufacturerUpdateTest(LoggedInTestCase):
    def setUp(self):
        super().setUp()
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.update_url = reverse(
            "taxi:manufacturer-update", args=[self.manufacturer.pk]
        )

    def test_update_success(self):
        response = self.client.post(
            self.update_url, {"name": "qwerty", "country": "Qwerty"}
        )
        self.assertRedirects(response, MANUFACTURER_LIST_URL)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "qwerty")

    def test_update_fail_invalid_data(self):
        response = self.client.post(
            self.update_url, {"name": "", "country": "Qwerty"}
        )
        self.assertEqual(response.status_code, 200)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "Toyota")


class PrivateManufacturerDeleteTest(LoggedInTestCase):
    def setUp(self):
        super().setUp()
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )

    def test_delete_success(self):
        response = self.client.post(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.pk])
        )
        self.assertRedirects(response, MANUFACTURER_LIST_URL)
        self.assertFalse(
            Manufacturer.objects.filter(pk=self.manufacturer.pk).exists()
        )


class PrivateManufacturerListTest(LoggedInTestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturers = [
            ("Toyota", "Japan"),
            ("Ford", "USA"),
            ("BMW", "Germany"),
            ("Renault", "France"),
            ("Fiat", "Italy"),
            ("Volvo", "Sweden"),
            ("Hyundai", "South Korea"),
        ]
        for name, country in manufacturers:
            Manufacturer.objects.create(name=name, country=country)

    def test_manufacturer_list_get(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertIn("manufacturer_list", response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["object_list"]), 5)

    def test_search_part_value(self):
        searched_value = "r"
        response = self.client.get(
            MANUFACTURER_LIST_URL, {"searched_value": searched_value}
        )

        manufacturers = response.context["manufacturer_list"]
        for man in manufacturers:
            self.assertTrue(searched_value in man.name.lower())

    def test_search_form_keeps_searched_value(self):
        searched_value = "r"
        response = self.client.get(
            MANUFACTURER_LIST_URL, {"searched_value": searched_value}
        )

        form = response.context["search_form"]
        self.assertIsInstance(form, SearchForm)
        self.assertEqual(form.initial["searched_value"], searched_value)
