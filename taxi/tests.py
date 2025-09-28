from __future__ import annotations

from typing import Iterable

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


# ---------- helpers ----------
def _usernames(qs: Iterable) -> set[str]:
    return {obj.username for obj in qs}


def _car_models(qs: Iterable) -> set[str]:
    return {obj.model for obj in qs}


def _manuf_names(qs: Iterable) -> set[str]:
    return {obj.name for obj in qs}


# ---------- driver search ----------
class DriverSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user_model = get_user_model()
        # usuário para login
        cls.user = user_model.objects.create_user(
            username="admin",
            password="adminpass123",
            first_name="Ad",
            last_name="Min",
            license_number="ADM00001",
        )
        # dados para busca
        user_model.objects.create_user(
            username="john",
            password="x",
            first_name="John",
            last_name="Doe",
            license_number="AAA12345",
        )
        user_model.objects.create_user(
            username="joanna",
            password="x",
            first_name="Joanna",
            last_name="D",
            license_number="BBB12345",
        )
        user_model.objects.create_user(
            username="alice",
            password="x",
            first_name="Alice",
            last_name="W",
            license_number="CCC12345",
        )

    def setUp(self) -> None:
        self.client.login(username="admin", password="adminpass123")

    def test_list_without_query_returns_all(self) -> None:
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        drv = response.context["driver_list"]
        expected = {"john", "joanna", "alice"}
        self.assertTrue(expected.issubset(_usernames(drv)))

    def test_search_by_username_filters_results(self) -> None:
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "jo"})
        self.assertEqual(response.status_code, 200)
        drv = response.context["driver_list"]
        self.assertEqual(_usernames(drv), {"john", "joanna"})

    def test_search_form_echoes_query(self) -> None:
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "alice"})
        self.assertContains(response, 'value="alice"', html=False)


# ---------- car search ----------
class CarSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            username="admin",
            password="adminpass123",
            first_name="Ad",
            last_name="Min",
            license_number="ADM00001",
        )

        audi = Manufacturer.objects.create(name="Audi")
        bmw = Manufacturer.objects.create(name="BMW")
        skoda = Manufacturer.objects.create(name="Skoda")

        Car.objects.create(model="A6", manufacturer=audi)
        Car.objects.create(model="X5", manufacturer=bmw)
        Car.objects.create(model="Fabia", manufacturer=skoda)

    def setUp(self) -> None:
        self.client.login(username="admin", password="adminpass123")

    def test_list_without_query_returns_all(self) -> None:
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        cars = response.context["car_list"]
        expected = {"A6", "X5", "Fabia"}
        self.assertTrue(expected.issubset(_car_models(cars)))

    def test_search_by_model_filters_results(self) -> None:
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "a"})
        self.assertEqual(response.status_code, 200)
        cars = response.context["car_list"]
        self.assertEqual(_car_models(cars), {"A6", "Fabia"})

    def test_search_form_echoes_query(self) -> None:
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "x"})
        self.assertContains(response, 'value="x"', html=False)


# ---------- manufacturer search ----------
class ManufacturerSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            username="admin",
            password="adminpass123",
            first_name="Ad",
            last_name="Min",
            license_number="ADM00001",
        )

        Manufacturer.objects.create(name="Audi")
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Skoda")

    def setUp(self) -> None:
        self.client.login(username="admin", password="adminpass123")

    def test_list_without_query_returns_all(self) -> None:
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        items = response.context["manufacturer_list"]
        expected = {"Audi", "BMW", "Skoda"}
        self.assertTrue(expected.issubset(_manuf_names(items)))

    def test_search_by_name_filters_results(self) -> None:
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "a"})
        self.assertEqual(response.status_code, 200)
        items = response.context["manufacturer_list"]
        self.assertEqual(_manuf_names(items), {"Audi", "Skoda"})

    def test_search_form_echoes_query(self) -> None:
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "sk"})
        self.assertContains(response, 'value="sk"', html=False)
