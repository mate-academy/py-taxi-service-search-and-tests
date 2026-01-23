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
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="best",
            country="best_country",
        )
        Manufacturer.objects.create(
            name="worse",
            country="worse_country",
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturers"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer-list.html")

    def test_search_manufacturer(self):
        Manufacturer.objects.create(
            name="best",
            country="best_country",
        )
        Manufacturer.objects.create(
            name="worse",
            country="worse_country",
        )
        response = self.client.get(MANUFACTURER_URL, {"name": "best"})
        object_list = response.context["manufacturer_list"]
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0].name, "best")
        self.assertContains(response, "best")
        self.assertNotContains(response, "worse")
