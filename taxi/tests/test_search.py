from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class SearchTestsBase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_user",
            password="test12345",
            license_number="ADM12345",
        )
        self.client.force_login(self.user)


class DriverSearchTests(SearchTestsBase):
    def setUp(self):
        super().setUp()
        get_user_model().objects.create_user(
            username="alice",
            password="test12345",
            license_number="ALI12345",
        )
        get_user_model().objects.create_user(
            username="bob",
            password="test12345",
            license_number="BOB12345",
        )

    def test_search_finds_driver(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "ali"}
        )
        self.assertContains(response, "alice")
        self.assertNotContains(response, "bob")

    def test_search_is_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "ALI"}
        )
        self.assertContains(response, "alice")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "zzz"}
        )
        self.assertNotContains(response, "alice")
        self.assertNotContains(response, "bob")
        self.assertContains(response, "There are no drivers")

    def test_empty_search_returns_all(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": ""}
        )
        self.assertContains(response, "alice")
        self.assertContains(response, "bob")

    def test_search_form_keeps_value(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "ali"}
        )
        self.assertEqual(
            response.context["search_form"].initial["username"], "ali"
        )


class CarSearchTests(SearchTestsBase):
    def setUp(self):
        super().setUp()
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        Car.objects.create(model="Camry", manufacturer=manufacturer)
        Car.objects.create(model="Corolla", manufacturer=manufacturer)

    def test_search_finds_car(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "cam"})
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Corolla")

    def test_search_no_results(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "zzz"})
        self.assertNotContains(response, "Camry")
        self.assertNotContains(response, "Corolla")

    def test_empty_search_returns_all(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertContains(response, "Camry")
        self.assertContains(response, "Corolla")

    def test_search_form_in_context(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertIn("search_form", response.context)


class ManufacturerSearchTests(SearchTestsBase):
    def setUp(self):
        super().setUp()
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")

    def test_search_finds_manufacturer(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "toy"}
        )
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "zzz"}
        )
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_search_form_in_context(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertIn("search_form", response.context)

    def test_search_works_with_pagination(self):
        for i in range(6):
            Manufacturer.objects.create(name=f"Brand{i}", country="X")
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Brand"}
        )
        self.assertEqual(len(response.context["manufacturer_list"]), 5)
        self.assertTrue(response.context["is_paginated"])
