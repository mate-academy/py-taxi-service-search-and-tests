from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/")


class PrivateManufacturerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for manufacturer_id in range(3):
            Manufacturer.objects.create(
                name=f"Test Name-{manufacturer_id}",
                country=f"Test Country-{manufacturer_id}",
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self) -> None:
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)

        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class SearchManufacturerViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="fghjkvbndfgh678"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Manufacturer1", country="Country1"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Manufacturer2", country="Country2"
        )

    def test_manufacturer_list_view_with_search(self):
        search_param = "?name=Manufacturer1"
        response = self.client.get(MANUFACTURER_URL + search_param)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manufacturer1")
        self.assertNotContains(response, "Manufacturer2")
