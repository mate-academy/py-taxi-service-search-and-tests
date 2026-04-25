from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Manufacturer.objects.create(name="Renault", country="France")
        Manufacturer.objects.create(name="BMW", country="Germany")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search_with_results(self):
        query_params = {"name": "R"}
        response = self.client.get(MANUFACTURER_URL, query_params=query_params)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers.filter(name__icontains=query_params["name"]))
        )

    def test_manufacturer_search_without_results(self):
        query_params = {"name": "No results"}
        response = self.client.get(MANUFACTURER_URL, query_params=query_params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            []
        )

    def test_manufacturer_create_successful(self):
        response = self.client.post(
            MANUFACTURER_CREATE_URL,
            data={
                "name": "Mazda",
                "country": "Japan"
            }
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
