from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Honda")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(
            response, "taxi/manufacturer_list.html"
        )


class ManufacturerSearchTest(TestCase):
    def setUp(self) -> None:
        Manufacturer.objects.create(name="Toyota")
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Honda")
        response = self.client.get(url, {"name": "a"})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(url, {"name": ""})
        self.assertEqual(response.status_code, 200)


class ManufacturerUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.url = reverse("taxi:manufacturer-update",
                           args=[self.manufacturer.id])
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_update_manufacturer_by_id(self):
        data = {"name": "Tesla", "country": "USA"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "Tesla")
        self.assertEqual(self.manufacturer.country, "USA")
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))


class ManufacturerDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA",
        )
        self.url = reverse("taxi:manufacturer-delete",
                           args=[self.manufacturer.id])
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_delete_manufacturer_by_id(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Manufacturer.objects.filter(
            id=self.manufacturer.id).exists())
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))


class ManufacturerCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.url = reverse("taxi:manufacturer-create")
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_create_manufacturer(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Toyota", "country": "Japan"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Japan")
