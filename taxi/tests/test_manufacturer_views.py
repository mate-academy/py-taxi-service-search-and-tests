from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer


MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
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

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Nissan")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name_returns_correct_results(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Nissan")
        response = self.client.get(MANUFACTURER_URL, {"name": "bm"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Nissan")

    def test_search_manufacturer_by_name_no_match(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Nissan")
        response = self.client.get(MANUFACTURER_URL, {"name": "Toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "BMW")
        self.assertNotContains(response, "Nissan")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            []
        )

    def test_search_manufacturer_without_query_returns_all(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Nissan")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertContains(response, "Nissan")
