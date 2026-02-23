from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

Manufacturer_url = reverse("taxi:manufacturer-list")


class PublicManufactureListView(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(Manufacturer_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufactureListView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12234",
            license_number="TST00001"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Aston Martin", country="England")
        Manufacturer.objects.create(name="Bugatti", country="France")

    def test_retrieve_manufacturer(self) -> None:
        response = self.client.get(Manufacturer_url)
        self.assertEqual(response.status_code, 200)
        manufacturerall = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturerall)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_by_manufacturer(self) -> None:
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Aston Martin"}
        )
        self.assertContains(response, "Aston Martin")
        self.assertNotContains(response, "Bugatti")
