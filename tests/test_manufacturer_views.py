from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)
        self.daewoo = Manufacturer.objects.create(
            name="Daewoo", country="Ukraine"
        )
        self.mazda = Manufacturer.objects.create(
            name="Mazda", country="Japan"
        )

    def test_manufacturer_list(self) -> None:
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_search(self) -> None:
        response = self.client.get(MANUFACTURER_URL, {"name": "dae"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertNotContains(response, "Mazda")
        self.assertContains(response, "Daewoo")
