from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURER_FORMAT_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerListView(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerListView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="Test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self) -> None:
        Manufacturer.objects.create(
            name="mercedes",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        response = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturer))
        self.assertTemplateUsed(response,
                                "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self) -> None:
        Manufacturer.objects.create(
            name="Mercedes",
            country="Germany"
        )
        toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        response = self.client.get(MANUFACTURER_FORMAT_URL, {"name": "Toy"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(toyota, response.context["manufacturer_list"])
        for manufacturer in response.context["manufacturer_list"]:
            self.assertIn("Toy", manufacturer.name)
